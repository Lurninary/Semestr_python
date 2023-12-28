from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from Resources.database import Ui_MainWindow
from youtubeAPI import YoutubeVideo


# Создание пользовательского виджета, который будет использоваться для отображения таблицы базы данных
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self, db_handler):
        super().__init__()
        self.setupUi(self)
        self.db_handler = db_handler
        self.dbTable.setAcceptDrops(True)

        self.dbSaveBtn.clicked.connect(self.save_to_db)
        self.dbDeleteBtn.clicked.connect(self.delete_from_db)
        self.dbLoadBtn.clicked.connect(self.fill_table)

    # Функция заполнения таблицы данными из базы данных
    def fill_table(self):
        self.dbTable.clear()
        items = self.db_handler.retrieve_items()
        headers = ['ID', 'Title', 'Duration', 'Views', 'Published', 'Thumbnail URL', 'URL']
        self.dbTable.setRowCount(len(items))
        self.dbTable.setColumnCount(len(headers))
        self.dbTable.setHorizontalHeaderLabels(headers)
        for i, item in enumerate(items):
            for j, field in enumerate(item):
                self.dbTable.setItem(i, j, QTableWidgetItem(str(field)))

    # Функция сохранения данных из таблицы в базу данных
    def save_to_db(self):
        self.db_handler.clear_table()
        for i in range(self.dbTable.rowCount()):
            record = {
                'id': int(self.dbTable.item(i, 0).text()),
                'title': self.dbTable.item(i, 1).text(),
                'duration': self.dbTable.item(i, 2).text(),
                'views': int(self.dbTable.item(i, 3).text()),
                'published': self.dbTable.item(i, 4).text(),
                'thumbnail_url': self.dbTable.item(i, 5).text(),
                'url': self.dbTable.item(i, 6).text()
            }
            self.db_handler.insert_record(record)

    # Функция удаления данных из таблицы и базы данных
    def delete_from_db(self):
        indexes = self.dbTable.selectedItems()
        if not indexes:
            QMessageBox.critical(self, 'Ошибка', 'Не выбран ни один элемент!')
            return
        for index in sorted(indexes, reverse=True):
            item_id = int(self.dbTable.item(index.row(), 0).text())
            self.db_handler.delete_item(item_id)
            self.dbTable.removeRow(index.row())

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            for url in e.mimeData().urls():
                self.load_video_from_url(url.toString())
                self.db_handler.insert_record(self.videoAPI.get_info_json())
            e.accept()

    def load_video_from_url(self, url):
        videoAPI = YoutubeVideo(url=url)
        self.add_video_to_list(videoAPI.get_info_json())