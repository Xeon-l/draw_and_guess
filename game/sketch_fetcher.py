"""Online sketch fetcher with local cache. Falls back to local assets."""
import os
import io
import hashlib
import threading
import requests
from PIL import Image

SKETCH_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sketches")
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# Baidu image search API (no key needed, returns thumbnail URLs)
BAIDU_SEARCH_URL = "https://image.baidu.com/search/acjson"
BAIDU_PARAMS_TEMPLATE = {
    "tn": "resultjson_com",
    "logid": "1234567890",
    "ipn": "rj",
    "ct": "201326592",
    "is": "",
    "fp": "result",
    "fr": "",
    "word": "",  # will be filled
    "queryWord": "",
    "cl": "2",
    "lm": "-1",
    "ie": "utf-8",
    "oe": "utf-8",
    "adpicid": "",
    "st": "-1",
    "z": "",
    "ic": "",
    "hd": "",
    "latest": "",
    "copyright": "",
    "s": "",
    "se": "",
    "tab": "",
    "width": "",
    "height": "",
    "face": "0",
    "istype": "2",
    "qc": "",
    "nc": "1",
    "expermode": "",
    "nojc": "",
    "isAsync": "",
    "pn": "0",
    "rn": "6",
    "gsm": "1e",
}

TIMEOUT = 5  # seconds


def _cache_path(word):
    """Get local cache file path for a word."""
    safe = hashlib.md5(word.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{safe}.png")


def _get_local_sketch(word):
    """Check local assets/sketches/ for a sketch."""
    path = os.path.join(SKETCH_DIR, f"{word}.png")
    if os.path.exists(path):
        return path
    return None


def _get_cached_sketch(word):
    """Check cache directory for a previously fetched sketch."""
    path = _cache_path(word)
    if os.path.exists(path):
        return path
    return None


def _fetch_baidu_image(word):
    """Fetch a sketch image from Baidu image search. Returns PIL Image or None."""
    try:
        params = dict(BAIDU_PARAMS_TEMPLATE)
        params["word"] = f"{word} 简笔画"
        params["queryWord"] = f"{word} 简笔画"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://image.baidu.com/",
        }

        resp = requests.get(BAIDU_SEARCH_URL, params=params, headers=headers, timeout=TIMEOUT)
        data = resp.json()

        # Try to get a thumbnail URL from results
        for item in data.get("data", []):
            thumb_url = item.get("thumbURL") or item.get("middleURL")
            if thumb_url:
                img_resp = requests.get(thumb_url, headers=headers, timeout=TIMEOUT)
                if img_resp.status_code == 200:
                    img = Image.open(io.BytesIO(img_resp.content))
                    return img.convert("RGB")
    except Exception:
        pass
    return None


def _save_to_cache(word, img):
    """Save fetched image to cache."""
    path = _cache_path(word)
    img.save(path, "PNG")


def get_sketch_path(word):
    """Get sketch image path for a word. Order: local → cache → fetch online."""
    # 1. Local assets
    local = _get_local_sketch(word)
    if local:
        return local, "local"

    # 2. Cache
    cached = _get_cached_sketch(word)
    if cached:
        return cached, "cache"

    # 3. Fetch online (synchronous for simplicity)
    img = _fetch_baidu_image(word)
    if img:
        img = img.resize((420, 300), Image.LANCZOS)
        _save_to_cache(word, img)
        return _cache_path(word), "online"

    return None, None


def prefetch_words(words, callback=None):
    """Prefetch sketches for a list of words in background thread."""
    def _worker():
        for word in words:
            path, source = get_sketch_path(word)
            if callback and path:
                callback(word, source)
    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
    return thread


def get_all_sketchable_words():
    """Return all words that have a sketch (local or cached)."""
    from game.words import ALL_WORDS
    result = []
    for entry in ALL_WORDS:
        word = entry["word"]
        local = _get_local_sketch(word)
        cached = _get_cached_sketch(word)
        if local or cached:
            result.append(word)
    return result
