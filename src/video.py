from googleapiclient.discovery import build
import os


class Video:

    def __init__(self, video_id: str):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        - id видео
        - название видео
        - ссылка на видео
        - количество просмотров
        - количество лайков"""
        self.video_id = video_id
        self.title = None
        self.url = None
        self.view_count = None
        self.likes = None

        self._get_video_info()

    def __str__(self):
        """
        магимческий метод для возвращения в строковом варианте названия канала
        """
        return self.title

    def _get_video_info(self):
        """
        метод для получения инфы о видео
        """
        api_key = os.environ.get('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video = youtube.videos().list(
            part='snippet,statistics',
            id=self.video_id
        ).execute()  # запрос к API и получение данных в json-подобном формате

        video_info = video['items'][0]['snippet']  # для хранения общей инфы о видео
        statistics = video['items'][0]['statistics']  # для хранения статистической инфы

        self.title = video_info['title']
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.view_count = int(statistics['viewCount'])
        self.likes = int(statistics['likeCount'])


class PLVideo(Video):
    """
   класс для видео `PLVideo`, наследуемый от класса Video
    """
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id

