from googleapiclient.discovery import build
import os


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key = os.environ.get('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)

        channel = youtube.channels().list(
            part='snippet,statistics',
            id=self.channel_id
        ).execute()  # запрос к API и получение данных в json-подобном формате

        channel_info = channel['items'][0]
        title = channel_info['snippet']['title']
        description = channel_info['snippet']['description']
        subscriber_count = channel_info['statistics']['subscriberCount']
        view_count = channel_info['statistics']['viewCount']
        video_count = channel_info['statistics']['videoCount']

        print(f"Название канала: {title}\n")
        print(f"Описание канала: {description}\n")
        print(f"Количество подписчиков: {subscriber_count}\n")
        print(f"Количество просмотров: {view_count}\n")
        print(f"Количество видео: {video_count}\n")