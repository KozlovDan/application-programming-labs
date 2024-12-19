import csv

class ImageIterator:
    def __init__(self, csv_path: str) -> None:
        self.csv_path = csv_path
        self.image_paths = []
        self.curr = 0
        self.load_annotations()

    def load_annotations(self):
        with open(self.csv_path, mode='r') as f :
            reader = csv.reader(f)
            next(reader)
            self.image_paths = [row[0] for row in reader]

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if self.curr < len(self.image_paths):
            image_path = self.image_paths[self.curr]
            self.curr += 1
            return image_path
        else:
            raise StopIteration
