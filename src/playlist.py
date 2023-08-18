import datetime
import os
import datetime as dt
import isodate
from googleapiclient.discovery import build


class PlayList:
    """Класс для ютуб-плейлистов"""
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.playlists = PlayList.get_service().playlists().list(
            part='snippet',
            id=self.__playlist_id
        ).execute()
        self.title = self.playlists['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    @property
    def total_duration(self) -> datetime.timedelta:
        video_response = self._get_playlist_videos()
        duration = dt.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self) -> str:
        video_response = self._get_playlist_videos()
        max_likes = 0
        video_id = ''
        for video in video_response['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_likes:
                max_likes = like_count
                video_id = video['id']
        return f'https://youtu.be/{video_id}'

    def _get_playlist_videos(self) -> dict:
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)
                                                          ).execute()
        return video_response
