def normalize_url(url: str) -> str:
    """Lowercase, https://, no www., no trailing slash."""
    url = url.strip().lower()
    if url.startswith("http://"):
        url = "https://" + url[7:]
    elif not url.startswith("https://"):
        url = "https://" + url
    if url.startswith("https://www."):
        url = "https://" + url[12:]
    return url.rstrip("/")
