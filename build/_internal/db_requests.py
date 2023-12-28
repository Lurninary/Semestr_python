import sqlite3
from sqlite3 import Error


# Класс для работы с базой данных
class DatabaseHandler:
    def __init__(self, db_name='videos.db'):
        self.conn = self.connect(db_name)  # Подключение к базе данных
        self.create_table()  # Создание таблицы в базе данных

    # Метод подключения к базе данных
    def connect(self, db_name):
        try:
            conn = sqlite3.connect(db_name)
            return conn
        except Error as e:
            print(e)

    # Метод создания таблицы в базе данных
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
         CREATE TABLE IF NOT EXISTS items (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT,
             duration TEXT,
             views INT,
             published DATE,
             thumbnail_url TEXT,
             url TEXT
         )
     ''')
        self.conn.commit()

    # Метод вставки записи в таблицу
    def insert_record(self, record):
        cursor = self.conn.cursor()
        cursor.execute('''
         INSERT INTO items (id, title, duration, views, published, thumbnail_url, url)
         VALUES (?, ?, ?, ?, ?, ?, ?)
     ''', (self.get_items_count() + 1, record['title'], record['duration'], record['views'], record['published'],
           record['thumbnail_url'], record['url']))
        self.conn.commit()

    # Метод обновления записи в таблице
    def update_item(self, record):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE items SET title = ?, duration = ?, views = ?, published = ?, thumbnail_url = ?, url = ?",
                       (
                           record.title, record.duration, record.views, record.published, record.thumbnail_url,
                           record.url))
        self.conn.commit()

    # Метод удаления записи из таблицы
    def delete_item(self, item_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        self.conn.commit()

    # Метод очистки таблицы
    def clear_table(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM items')
        self.conn.commit()

    # Метод получения всех записей из таблицы
    def retrieve_items(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        return items

    # Метод получения количества записей в таблице
    def get_items_count(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM items')
        count = cursor.fetchone()[0]
        return count
