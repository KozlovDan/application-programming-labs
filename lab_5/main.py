import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from Iterator import ImageIterator

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Птичий смотритель")

        self.image_iterator = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.image_label = QLabel("Выберите файл аннотации", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.select_annotation_button = QPushButton("Выбрать файл аннотации", self)
        self.select_annotation_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_annotation_button)

        self.next_image_button = QPushButton("Следующее изображение", self)
        self.next_image_button.clicked.connect(self.show_next_image)
        self.next_image_button.setEnabled(False)
        self.layout.addWidget(self.next_image_button)

    def select_file(self) -> None:
        """
                Выбирает файл аннотации .csv
        """
        annotation_file, _ = QFileDialog.getOpenFileName(self, "Выберите файл аннотации", filter="CSV Files (*.csv)")
        if annotation_file:
            self.image_iterator = ImageIterator(annotation_file)
            self.next_image_button.setEnabled(True)
            self.show_next_image()

    def show_next_image(self) -> None:
        """
            Перелистывает на следующее изображение
        """
        if self.image_iterator:
            try:
                absolute_path = next(self.image_iterator)
                if os.path.exists(absolute_path):
                    pixmap = QPixmap(absolute_path)
                    self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
                else:
                    self.image_label.setText(f"Файл не найден: {absolute_path}")
            except StopIteration:
                self.image_label.setText("Изображения закончились")
                self.next_image_button.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec_())