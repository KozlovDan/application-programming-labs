import os
import csv
import argparse
from icrawler import ImageDownloader
from icrawler.builtin import GoogleImageCrawler


def download_images(keyword: str, num_images: int, download_path: str) -> None:
    """
    Скачивает изображения по заданному ключевому слову.
    :param keyword: Ключевое слово для поиска изображений (str).
    :param num_images: Количество изображений для загрузки (int).
    :param download_path: Путь к папке для сохранения загруженных изображений (str).
    :return: None
    """
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    crawler = GoogleImageCrawler(storage={"root_dir": download_path})
    crawler.crawl(keyword=keyword, max_num=num_images)


def annotation_maker(download_path: str, csv_path: str) -> None:
    """
    Создает .csv-файл с аннотацией для загруженных изображений.
    :param download_path: Путь к папке с изображениями (str).
    :param csv_path: Путь к .csv-файлу для сохранения аннотации (str).
    :return: None
    """
    with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["absolute_path", "relative_path"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for directory, _, files in os.walk(download_path):
            for file in files:
                absolute_path = os.path.join(directory, file)
                relative_path = os.path.relpath(absolute_path, download_path)
                writer.writerow({"absolute_path": absolute_path, "relative_path": relative_path})


class ImageIterator:
    def __init__(self, csv_path: str) -> None:
        """
               Инициализирует итератор изображений.
               :param csv_path: Путь к файлу с аннотациями.
               """
        self.csv_path = csv_path
        self.image_paths = []
        self.curr = 0 # Индекс
        self.load_annotations()

    def load_annotations(self):
        """
        Загружает аннотации изображений из .csv файла.
        """
        with open(self.csv_path, mode='r') as f :
            reader = csv.reader(f)
            next(reader)
            self.image_paths = [row[0] for row in reader]

    def __iter__(self):
        """
        Возвращает объект итератора.
        """
        return self  # Возвращаем сам объект, чтобы он был итерируемым

    def __next__(self) -> str:
        """
        Возвращает следующий путь к изображению.
        :return: Путь к следующему изображению.
        :raise StopIteration: Когда достигнут конец списка изображений.
        """
        if self.curr < len(self.image_paths):
            image_path = self.image_paths[self.curr]
            self.curr += 1
            return image_path
        else:
            raise StopIteration

# Функция для демонстрации итератора
def print_images(image_iterator)-> None:
    """
    Выводит пути изображений в цикле
    :param image_iterator: Итератор.
    """
    for img_path in image_iterator:
        print(img_path)

def main():
    parser = argparse.ArgumentParser(description="Скачать изображения коров и создать аннотацию.")
    parser.add_argument("keyword", type=str, help="Ключевое слово для поиска изображений.")
    parser.add_argument("num_images", type=int, help="Количество изображений для загрузки (от 50 до 1000).")
    parser.add_argument("download_path", type=str, help="Путь к папке, в которой сохранениются изображения.")
    parser.add_argument("csv_path", type=str, help="Путь к файлу аннотации.")

    args = parser.parse_args()

    download_images(args.keyword, args.num_images, args.download_path)
    annotation_maker(args.download_path, args.csv_path)

    image_iterator = ImageIterator(args.csv_path)

    print_images(image_iterator) # Пример использования итератора

if __name__ == '__main__':
    main()