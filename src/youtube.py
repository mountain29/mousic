import yt_dlp
from ytmusicapi import YTMusic
from urllib.parse import quote

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'extract_flat': True,
    'skip_download': True,
}

class yt:
    @staticmethod
    def search(query: str, size: int = 1):
        from ytmusicapi import YTMusic

        ytm = YTMusic()
        results = ytm.search(f"{query}", filter="songs", limit=size)
        results = results[:size]
        return results

# print(yt.search("son tung", size=10))
