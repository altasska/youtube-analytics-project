from googleapiclient.discovery import build
from src.video import PLVideo
import os
import datetime


class PlayList:
    """
    Экземпляр инициализируется по _id_ плейлиста. Дальше все данные будут подтягиваться по API
    - название плейлиста
    - ссылка на плейлист
    """

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.title = None
        self.url = None
        self.youtube = self._create_YT_api()

        self._get_playlist_info()

    def _create_YT_api(self):
        """
        метод для создания объекта только один раз при инициализации класса
        """
        api_key = os.environ.get('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def _get_playlist_info(self):
        """
        метод для получения нужной инфы
        """
        playlist = self.youtube.playlists().list(
            part='snippet',
            id=self.playlist_id
        ).execute()  # запрос к API и получение данных в json-подобном формате

        playlist_info = playlist['items'][0]['snippet']  # для хранения общей информации о плейлисте

        self.title = playlist_info['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        """
        метод для возвроращения объекта класса `datetime.timedelta` с суммарной длительностью плейлиста
        """

        video_response = self.youtube.playlistItems().list(
            part='contentDetails',
            playlistId=self.playlist_id,
        ).execute()  # запрос к API и получение данных в json-подобном формате

        total_duration = datetime.timedelta()

        for item in video_response['items']:
            video_id = item['contentDetails']['videoId']
            video = PLVideo(video_id, self.playlist_id)
            total_duration += video.duration

        return total_duration

    def show_best_video(self):
        """
        метод для возвращения ссылки на самое популярное видео из плейлиста (по количеству лайков)
        """

        video_response = self.youtube.playlistItems().list(
            part='contentDetails',
            playlistId=self.playlist_id,
        ).execute()  # запрос к API и получение данных в json-подобном формате

        best_video_id = None
        best_likes = 0

        for item in video_response['items']:
            video_id = item['contentDetails']['videoId']
            video = PLVideo(video_id, self.playlist_id)
            if video.like_count > best_likes:
                best_video_id = video_id
                best_likes = video.like_count

        return f"https://youtu.be/{best_video_id}"
