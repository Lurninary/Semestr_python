# Поиск видео

Это приложение позволяет пользователям искать видео на YouTube и сохранять их в локальную базу данных. Вы можете просматривать сохраненные видео, а также загружать их из базы данных.

# Возможности

* Искать видео на YouTube по запросу или по URL
* Просмотреть детали каждого видео, включая название, длительность, количество просмотров, дату публикации и миниатюру
* Сохранять найденные видео в локальной базе данных
* Просматривать сохраненные видео в отдельном окне
* Удалять видео из списка и из базы данных
# Использование
* Введите запрос в поле поиска и нажмите кнопку "Search". Приложение вернет список видео, соответствующих вашему запросу.
* Чтобы сохранить видео, выберите его из списка и нажмите кнопку "Save". Вы получите подтверждение, прежде чем видео будет сохранено.
* Чтобы просмотреть сохраненные видео, нажмите кнопку "View Saved". Это откроет новое окно, где вы можете просмотреть все сохраненные видео.
* Чтобы удалить видео из списка и из базы данных, выберите его в окне просмотра и нажмите кнопку "Delete".
# Зависимости
Это приложение использует следующие библиотеки:

* PyQt5 для создания графического интерфейса пользователя
* Requests для отправки HTTP-запросов к YouTube API
* SQLite3 для работы с локальной базой данных
# Установка
Клонируйте репозиторий и установите необходимые библиотеки:

```git clone https://github.com/Lurninary/Semestr_python.git```

```pip install -r requirements.txt```
# Запустите приложение:

```python main.py```
