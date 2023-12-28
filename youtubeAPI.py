import requests
from const import filters


# Класс для работы с YouTube API
class YoutubeVideo:
    def __init__(self, url=None, query=None, filter=None):
        self.title = None
        self.duration = None
        self.published = None
        self.views = None
        self.thumbnail_url = None
        self.url = None
        self.videos = []

        if url:
            self.get_info_from_url(url)
        elif query:
            self.get_info_from_query(query, filter=filter)

    # Метод получения информации о видео по его URL
    def get_info_from_url(self, url):
        try:
            api_key = 'AIzaSyA7Dj7V_p_23QPI-2YunOVqWlgV06OrEek'
            video_id = url.removeprefix("www.youtube.com/watch?v=")
            api_url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails,id&id={video_id}&key={api_key}"
            response = requests.get(api_url).json()
            self.title = response['items'][0]['snippet']['title']
            duration_str = response['items'][0]['contentDetails']['duration']
            self.duration = self.parse_duration(duration_str)
            self.views = response['items'][0]['statistics']['viewCount']
            self.published = response['items'][0]['snippet']['publishedAt']
            self.thumbnail_url = response['items'][0]['snippet']['thumbnails']['medium']['url']
            self.url = url
        except Exception as e:
            print(f"Error fetching video info: {e}")
            raise

    # Метод получения информации о видео по запросу
    def get_info_from_query(self, query, filter=None):
        self.videos = []
        api_key = 'AIzaSyA7Dj7V_p_23QPI-2YunOVqWlgV06OrEek'
        api_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults=10&key={api_key}"
        if (filter):
            api_url += f"&order={filters[filter]}"

        response = requests.get(api_url).json()
        for video in response['items']:
            video_id = video['id']['videoId']
            self.get_info_from_url(f"www.youtube.com/watch?v={video_id}")
            self.videos.append(self.get_info_json())

    # Метод парсинга продолжительности видео
    def parse_duration(self, duration_str):
        duration_str = duration_str[2:]
        duration = ''
        duration_str = duration_str.replace('H', ':').replace('M', ':').replace('S', '')
        for part in duration_str.split(':'):
            if len(part) < 2:
                if part != 0:
                    duration += '0' + part
                else:
                    duration += '00'
            else:
                duration += part
            duration += ':'
        return duration[:8] if len(duration_str.split(":")) == 3 else "00:" + duration[:5] \
            if len(duration_str.split(":")) == 2 else "00:00:" + duration[:2]

    # Метод печати информации о видео
    def print_info(self):
        for video in self.videos:
            print(f"Title: {video['title']}")
            print(f"Duration: {video['duration']}")
            print(f"Views: {video['views']}")
            print(f"Published at: {video['published']}")
            print(f"Thumbnail URL: {video['thumbnail_url']}")
            print("\n")

    # Метод возвращения информации о видео в формате JSON
    def get_info_json(self):
        info = {
            "title": self.title,
            "duration": self.duration,
            "views": self.views,
            "published": self.published,
            "thumbnail_url": self.thumbnail_url,
            "url": self.url
        }
        return info
