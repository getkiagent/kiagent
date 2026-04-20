#!/usr/bin/env python3
"""
Instagram / TikTok / YouTube post summarizer.

Usage:
    python tools/summarize_reel.py <url>

Pipeline:
  1. Download post via yt-dlp.
  2. If the file has an audio stream -> transcribe locally with Whisper (base).
  3. If the file is silent video or an image -> extract frames and describe
     them with Claude Vision (haiku).
  4. Save JSON to /reels/ and print it to stdout.

Requires: ffmpeg on PATH (auto-detected from winget), ANTHROPIC_API_KEY in .env
for the vision fallback.
"""

import sys
import os
import re
import json
import glob
import subprocess
import tempfile
import base64
import mimetypes
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


VISION_MODEL = "claude-haiku-4-5-20251001"
FRAMES_PER_VIDEO = 6
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# Skip links back to the source platforms — they are not external references.
LINK_HOST_BLOCKLIST = {
    "instagram.com", "www.instagram.com",
    "tiktok.com", "www.tiktok.com", "vm.tiktok.com",
    "youtube.com", "www.youtube.com", "youtu.be",
    "twitter.com", "www.twitter.com", "x.com",
}
LINK_MAX = 5
LINK_TIMEOUT = 10
LINK_SNIPPET_CHARS = 1500


# --- ffmpeg auto-discovery ----------------------------------------------------
def ensure_ffmpeg_on_path() -> str | None:
    from shutil import which
    if which("ffmpeg"):
        return os.path.dirname(which("ffmpeg"))
    candidates = glob.glob(
        os.path.expanduser(
            r"~\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin"
        )
    )
    for cand in candidates:
        if os.path.isfile(os.path.join(cand, "ffmpeg.exe")):
            os.environ["PATH"] = cand + os.pathsep + os.environ.get("PATH", "")
            return cand
    return None


# --- download -----------------------------------------------------------------
def _scrape_ig_cover(url: str, post_id: str, out_dir: str) -> str | None:
    """Fallback for IG image-only posts: grab og:image cover and save as jpg."""
    import requests

    try:
        r = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15,
        )
        if r.status_code != 200:
            return None
        m = re.search(
            r'<meta property="og:image" content="([^"]+)"', r.text
        )
        if not m:
            return None
        img_url = m.group(1).replace("&amp;", "&")
        img = requests.get(img_url, timeout=15)
        if img.status_code != 200:
            return None
        path = os.path.join(out_dir, f"{post_id}.jpg")
        with open(path, "wb") as f:
            f.write(img.content)
        return path
    except Exception:
        return None


def download_media(url: str, out_dir: str) -> tuple[str | None, dict, dict]:
    """Download raw media. Returns (path, metadata, warnings). path is None for text-only tweets."""
    import yt_dlp

    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(out_dir, "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }
    warnings: dict = {}

    is_twitter = any(h in url.lower() for h in ("twitter.com/", "x.com/"))

    if is_twitter:
        import requests as _req
        # Use oEmbed to get tweet text without login.
        tweet_id = urlparse(url).path.strip("/").split("/")[-1].split("?")[0]
        oembed_url = f"https://publish.twitter.com/oembed?url=https://twitter.com/i/status/{tweet_id}"
        try:
            resp = _req.get(oembed_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            oembed = resp.json() if resp.status_code == 200 else {}
        except Exception:
            oembed = {}
        html = oembed.get("html", "")
        import re as _re
        tweet_text = _re.sub(r"\s+", " ", _re.sub("<[^>]+>", " ", html)).strip()
        # Strip HTML entities
        tweet_text = tweet_text.replace("&mdash;", "—").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        metadata = {
            "id": tweet_id,
            "title": None,
            "uploader": oembed.get("author_name"),
            "uploader_id": None,
            "duration": None,
            "view_count": None,
            "like_count": None,
            "description": tweet_text or None,
            "url": url,
        }
        # Try to download video (needs login; skip gracefully if not available).
        cookie_file = Path(__file__).resolve().parent / "x_cookies.txt"
        if cookie_file.exists():
            ydl_opts["cookiefile"] = str(cookie_file)
        try:
            meta_opts = {**ydl_opts, "skip_download": True, "ignoreerrors": True, "quiet": True}
            with yt_dlp.YoutubeDL(meta_opts) as ydl:
                info = ydl.extract_info(url, download=False) or {}
            formats = info.get("formats") or []
            has_video = any(f.get("vcodec", "none") not in ("none", None) for f in formats)
            if has_video:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.extract_info(url, download=True)
                downloaded = glob.glob(os.path.join(out_dir, f"{tweet_id}.*"))
                if downloaded:
                    return downloaded[0], metadata, warnings
        except Exception:
            pass
        return None, metadata, warnings

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except yt_dlp.utils.DownloadError as e:
        # yt-dlp refuses image-only IG posts with "no video in this post".
        # Metadata is still reachable via skip_download extractor.
        if "no video in this post" not in str(e).lower():
            raise
        meta_opts = {**ydl_opts, "skip_download": True, "ignoreerrors": True}
        with yt_dlp.YoutubeDL(meta_opts) as ydl:
            info = ydl.extract_info(url, download=False) or {}
        info.setdefault("_type", "playlist")
        info.setdefault("entries", [])

    # Playlists (carousels) return an info dict with entries; we pick first
    # but keep playlist-level fields (description, uploader) which the entry lacks.
    if info.get("_type") == "playlist":
        entries = info.get("entries") or []
        playlist_fields = {
            k: info.get(k) for k in ("description", "uploader", "uploader_id", "title")
            if info.get(k)
        }
        if not entries:
            # Image-only IG carousel: yt-dlp can't fetch images. Fall back to
            # scraping the og:image cover so vision at least sees slide 1.
            post_id = info.get("id") or urlparse(url).path.rstrip("/").split("/")[-1]
            cover = _scrape_ig_cover(url, post_id, out_dir)
            if not cover:
                raise RuntimeError("Playlist has no downloadable entries")
            warnings["carousel_fallback"] = "cover_only"
            metadata = {
                "id": post_id,
                "title": playlist_fields.get("title"),
                "uploader": playlist_fields.get("uploader"),
                "uploader_id": playlist_fields.get("uploader_id"),
                "duration": None,
                "view_count": None,
                "like_count": None,
                "description": playlist_fields.get("description"),
                "url": url,
            }
            return cover, metadata, warnings
        info = {**entries[0], **playlist_fields}

    downloaded = glob.glob(os.path.join(out_dir, f"{info['id']}.*"))
    if not downloaded:
        raise RuntimeError(f"yt-dlp finished but no file for id {info['id']}")
    media_path = downloaded[0]

    metadata = {
        "id": info.get("id"),
        "title": info.get("title"),
        "uploader": info.get("uploader"),
        "uploader_id": info.get("uploader_id"),
        "duration": info.get("duration"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "description": info.get("description"),
        "url": url,
    }
    return media_path, metadata, warnings


# --- classification -----------------------------------------------------------
def probe_streams(path: str) -> dict:
    """Return {has_audio, has_video, duration} for the media file."""
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "stream=codec_type:format=duration",
            "-of", "json", path,
        ],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(result.stdout)
    codec_types = [s.get("codec_type") for s in data.get("streams", [])]
    duration = float(data.get("format", {}).get("duration") or 0)
    return {
        "has_audio": "audio" in codec_types,
        "has_video": "video" in codec_types,
        "duration": duration,
    }


# --- whisper path -------------------------------------------------------------
def transcribe_audio(media_path: str, work_dir: str) -> dict:
    """Extract mp3 via ffmpeg, transcribe with Whisper."""
    import whisper

    mp3_path = os.path.join(work_dir, "audio.mp3")
    subprocess.run(
        ["ffmpeg", "-y", "-i", media_path, "-vn", "-q:a", "2", mp3_path],
        check=True, capture_output=True,
    )
    model = whisper.load_model("base")
    result = model.transcribe(mp3_path, fp16=False)
    return {
        "mode": "transcript",
        "language": result.get("language"),
        "text": (result.get("text") or "").strip(),
    }


# --- vision path --------------------------------------------------------------
def extract_frames(video_path: str, duration: float, work_dir: str) -> list[str]:
    """Extract evenly spaced frames from a video. Returns list of jpg paths."""
    frames = []
    n = FRAMES_PER_VIDEO
    for i in range(n):
        # sample at the middle of each segment to avoid black edges
        t = duration * (i + 0.5) / n
        out = os.path.join(work_dir, f"frame_{i:02d}.jpg")
        subprocess.run(
            [
                "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", video_path,
                "-frames:v", "1", "-q:v", "3", out,
            ],
            check=True, capture_output=True,
        )
        if os.path.isfile(out):
            frames.append(out)
    return frames


def describe_with_vision(image_paths: list[str], caption: str | None) -> dict:
    """Send images to Claude Vision for text extraction + summary."""
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    import anthropic

    client = anthropic.Anthropic()
    content: list[dict] = []
    for p in image_paths:
        mime = mimetypes.guess_type(p)[0] or "image/jpeg"
        with open(p, "rb") as f:
            b64 = base64.standard_b64encode(f.read()).decode("ascii")
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": mime, "data": b64},
        })

    prompt = (
        "These images are frames from an Instagram/TikTok post (or a single-image post). "
        "For each distinct slide/frame, extract ALL visible text verbatim "
        "and describe any non-text visuals in one line. "
        "Dedupe near-identical frames. "
        "Output as markdown with a section per slide (### Slide N), then a final "
        "'### Summary' section with 2-3 sentences on the overall message. "
        "Respond in the same language as the post text."
    )
    if caption:
        prompt += f"\n\nPost caption for context:\n{caption}"

    content.append({"type": "text", "text": prompt})

    msg = client.messages.create(
        model=VISION_MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": content}],
    )
    text = "".join(b.text for b in msg.content if b.type == "text")
    return {
        "mode": "vision",
        "model": VISION_MODEL,
        "frame_count": len(image_paths),
        "text": text.strip(),
    }


# --- link following -----------------------------------------------------------
URL_RE = re.compile(r"https?://[^\s)\]\}<>\"']+", re.IGNORECASE)


def extract_urls(caption: str | None) -> list[str]:
    """Return unique external URLs from caption, preserving order."""
    if not caption:
        return []
    seen: set[str] = set()
    out: list[str] = []
    for raw in URL_RE.findall(caption):
        url = raw.rstrip(".,;:!?")
        host = urlparse(url).netloc.lower()
        if not host or host in LINK_HOST_BLOCKLIST:
            continue
        if url in seen:
            continue
        seen.add(url)
        out.append(url)
    return out


def fetch_link(url: str) -> dict:
    """Fetch a URL and extract title, meta description, and a text snippet."""
    import requests
    from bs4 import BeautifulSoup

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }
    try:
        r = requests.get(url, headers=headers, timeout=LINK_TIMEOUT, allow_redirects=True)
        r.raise_for_status()
    except Exception as e:
        return {"url": url, "error": str(e)}

    ctype = r.headers.get("content-type", "").lower()
    if "html" not in ctype and "text" not in ctype:
        return {"url": url, "final_url": r.url, "content_type": ctype, "error": "non-html"}

    soup = BeautifulSoup(r.text, "html.parser")
    title = (soup.title.string.strip() if soup.title and soup.title.string else None)
    desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find(
        "meta", attrs={"property": "og:description"}
    )
    description = desc_tag.get("content", "").strip() if desc_tag else None

    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.decompose()
    body_text = re.sub(r"\s+", " ", soup.get_text(" ")).strip()
    snippet = body_text[:LINK_SNIPPET_CHARS]

    return {
        "url": url,
        "final_url": r.url,
        "title": title,
        "description": description,
        "snippet": snippet,
    }


def follow_links(caption: str | None) -> list[dict]:
    urls = extract_urls(caption)[:LINK_MAX]
    return [fetch_link(u) for u in urls]


# --- main ---------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/summarize_reel.py <url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1].strip()

    if not ensure_ffmpeg_on_path():
        print(
            "ERROR: ffmpeg not found. Install via: winget install Gyan.FFmpeg",
            file=sys.stderr,
        )
        sys.exit(2)

    with tempfile.TemporaryDirectory() as tmp:
        try:
            media_path, meta, warnings = download_media(url, tmp)
        except Exception as e:
            print(f"ERROR download: {e}", file=sys.stderr)
            sys.exit(3)

        if media_path is None:
            result = {"mode": "text", "language": None, "text": meta.get("description") or ""}
        else:
            ext = Path(media_path).suffix.lower()
            try:
                if ext in IMAGE_EXTS:
                    result = describe_with_vision([media_path], meta.get("description"))
                else:
                    streams = probe_streams(media_path)
                    if streams["has_audio"]:
                        result = transcribe_audio(media_path, tmp)
                    else:
                        frames = extract_frames(media_path, streams["duration"], tmp)
                        if not frames:
                            raise RuntimeError("no frames extracted from silent video")
                        result = describe_with_vision(frames, meta.get("description"))
            except Exception as e:
                print(f"ERROR process: {e}", file=sys.stderr)
                sys.exit(4)

    linked_pages = follow_links(meta.get("description"))

    reels_dir = Path(__file__).resolve().parent.parent / "reels"
    reels_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = reels_dir / f"{timestamp}_{meta['id']}.json"

    output = {**meta, **result, "linked_pages": linked_pages, **warnings, "timestamp": timestamp}
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
