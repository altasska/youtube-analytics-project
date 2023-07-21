from googleapiclient.discovery import build
import os
import isodate


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
        self.like_count = None

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
        try:

            api_key = os.environ.get('API_KEY')
            youtube = build('youtube', 'v3', developerKey=api_key)
            video = youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=self.video_id
            ).execute()  # запрос к API и получение данных в json-подобном формате

            if 'items' in video and len(video['items']) > 0:  # если есть данные о видео

                video_info = video['items'][0]['snippet']  # для хранения общей инфы о видео
                statistics = video['items'][0]['statistics']  # для хранения статистической инфы
                content_details = video['items'][0][
                    'contentDetails']  # для хранения дополнительной инфы, в т.ч и о длительности видео

                self.title = video_info['title']
                self.url = f"https://www.youtube.com/watch?v={self.video_id}"
                self.view_count = int(statistics['viewCount'])
                self.like_count = int(statistics['likeCount'])
                duration_string = content_details['duration']  # данные в строковом формате ISO 8601
                self.duration = self._parse_duration(duration_string)  # преобразование в читабельный формат

            else:
                # если данных о видео нет
                self.title = None
                self.url = None
                self.view_count = None
                self.like_count = None

        except Exception as ex:

            self.title = None
            self.like_count = None

    def _parse_duration(self, duration_string):
        return isodate.parse_duration(duration_string)  # возвращает объект <class 'datetime.timedelta'>


class PLVideo(Video):
    """
   класс для видео `PLVideo`, наследуемый от класса Video
    """

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
