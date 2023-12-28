import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QWidget, QMessageBox
from Resources.mainUI import Ui_MainWindow
from Resources.video import Ui_Form
from db_window import MyWidget
from youtubeAPI import YoutubeVideo
from db_requests import DatabaseHandler
from const import filters


# Создание пользовательского виджета, который будет использоваться для отображения информации о видео
class CustomWidget(QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        super(CustomWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)


# Основное приложение поиска видео
class SearchApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.videoAPI = None
        self.db_handler = DatabaseHandler()
        self.db_window = MyWidget(self.db_handler)

        # Добавление фильтров в выпадающий список
        self.sortFilters.addItem('')
        for filter in filters:
            self.sortFilters.addItem(filter)

        # Связывание кнопок с соответствующими функциями
        self.searchBtn.clicked.connect(self.search)
        self.saveBtn.clicked.connect(self.on_saveBtn_clicked)
        self.viewSaved.clicked.connect(self.open_db_window)
        self.loadBtn.clicked.connect(self.load_data_from_db)

    # Функция поиска видео
    def search(self):
        query = self.searchLine.text()
        if not query:
            QMessageBox.critical(self, 'Ошибка', 'Поле поиска не должно быть пустым!')
            return
        self.listWidget.clear()
        if "www.youtube.com/watch?v=" in query:
            self.videoAPI = YoutubeVideo(url=query)
            self.add_video_to_list(self.videoAPI.get_info_json())
        else:
            self.videoAPI = YoutubeVideo(query=query, filter=self.sortFilters.currentText())
            for video_info in self.videoAPI.videos:
                QApplication.processEvents()
                self.add_video_to_list(video_info)

    # Функция добавления видео в список
    def add_video_to_list(self, video_info):
        item = QListWidgetItem()
        widget = CustomWidget()
        item.setSizeHint(widget.size())

        widget.Name.setText(video_info['title'])
        widget.Duration.setText(video_info['duration'])
        widget.Views.setText(video_info['views'])
        widget.Published.setText(video_info['published'])

        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(video_info['thumbnail_url']).content)
        pixmap = pixmap.scaled(widget.imageLabel.size())
        widget.imageLabel.setPixmap(pixmap)

        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, widget)

    # Функция сохранения видео
    def on_saveBtn_clicked(self):
        item = self.listWidget.currentItem()
        if item is None:
            QMessageBox.critical(self, 'Ошибка', 'Не выбран ни один элемент!')
            return
        index = self.listWidget.indexFromItem(item).row()
        reply = QMessageBox.question(self, 'Сохранение',
                                     "Вы уверены, что хотите сохранить?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.db_handler.insert_record(self.videoAPI.videos[index])

    # Функция открытия окна базы данных
    def open_db_window(self):
        self.db_window.show()

    # Функция загрузки данных из базы данных
    def load_data_from_db(self):
        items = self.db_handler.retrieve_items()
        self.listWidget.clear()
        for item in items:
            self.add_video_to_list({
                'title': item[1],
                'duration': item[2],
                'views': str(item[3]),
                'published': item[4],
                'thumbnail_url': item[5],
                'url': item[6]
            })


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SearchApp()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
