#!/usr/bin/env python3
"""
Instagram Reel transcriber.

Usage:
    python scripts/summarize_reel.py <reel_url>

Downloads audio via yt-dlp, transcribes locally with Whisper (base model),
prints transcript JSON to stdout, and saves a copy to /reels/.

No API keys required. Requires ffmpeg on PATH (or auto-detected from winget).
"""

import sys
import os
import json
import glob
import tempfile
from pathlib import Path
from datetime import datetime

# Force UTF-8 stdout on Windows so emoji/unicode in transcripts don't crash print
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# --- ffmpeg auto-discovery ----------------------------------------------------
def ensure_ffmpeg_on_path() -> str | None:
    """Ensure ffmpeg is callable. Returns ffmpeg dir if found, else None."""
    # Try shell first
    from shutil import which
    if which("ffmpeg"):
        return os.path.dirname(which("ffmpeg"))

    # Common winget install location
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


# --- core ---------------------------------------------------------------------
def download_audio(url: str, out_dir: str) -> tuple[str, dict]:
    """Download Instagram reel audio. Returns (audio_path, metadata)."""
    import yt_dlp

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(out_dir, "%(id)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        audio_path = os.path.join(out_dir, f"{info['id']}.mp3")
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
        return audio_path, metadata


def transcribe(audio_path: str, model_name: str = "base") -> dict:
    """Transcribe audio with local Whisper."""
    import whisper

    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path, fp16=False)
    return {
        "language": result.get("language"),
        "text": (result.get("text") or "").strip(),
    }


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python scripts/summarize_reel.py <instagram_reel_url>",
            file=sys.stderr,
        )
        sys.exit(1)

    url = sys.argv[1].strip()

    ffmpeg_dir = ensure_ffmpeg_on_path()
    if not ffmpeg_dir:
        print(
            "ERROR: ffmpeg not found. Install via: winget install Gyan.FFmpeg",
            file=sys.stderr,
        )
        sys.exit(2)

    with tempfile.TemporaryDirectory() as tmp:
        try:
            audio_path, meta = download_audio(url, tmp)
        except Exception as e:
            print(f"ERROR download: {e}", file=sys.stderr)
            sys.exit(3)

        try:
            transcript = transcribe(audio_path)
        except Exception as e:
            print(f"ERROR transcribe: {e}", file=sys.stderr)
            sys.exit(4)

    # Save artifact
    reels_dir = Path(__file__).resolve().parent.parent / "reels"
    reels_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = reels_dir / f"{timestamp}_{meta['id']}.json"

    output = {
        **meta,
        **transcript,
        "timestamp": timestamp,
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Stdout for the caller (Claude reads this)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
