import os

from googleapiclient.discovery import build


class Video:
    """Класс для ютуб-видео"""
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.playlists = Video.get_service().videos().list(
            part='snippet,statistics',
            id=self.video_id
        ).execute()
        self.title = self.playlists['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/{self.video_id}'
        self.view_count = self.playlists['items'][0]['statistics']['viewCount']
        self.like_count = self.playlists['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)


class PLVideo(Video):
    """Класс для ютуб-видео c плейлистами"""
    def __init__(self, video_id: str, plist_id: str) -> None:
        super().__init__(video_id)
        self.plist_id = plist_id

    def __str__(self):
        return self.title
