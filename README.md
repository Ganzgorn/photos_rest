### Запуск

Для запуска нужно выполнить 

manage.py syncdb

manage.py runserver

### ТЗ
Необходмо разработать REST API каталога фотографий.

API должно давать следующие возможности:

1. Загрузить фотографию, выбрать для нее цвет рамки фотографии с необязательной прозрачностью (RGB или RGBA), название фотографии. Также должны сохраняться данные о времени загрузки и пользователе, загрузившем файл.

2. Просматривать информацию о загруженной фотографии. 

3. Редактировать название и фоновый цвет фотографии.

4. Удалять фотографию.

5. Просматривать список фотографий пользователя с сортировкой по названию или времени добавления.

6. Просматривать список фотографий пользователя с постраничным выводом по 10, 50, 100 фотографий.

7. Просматривать список фотографий пользователя за конкретную дату.

8. Искать фотографию пользователя по частичному совпадению названия.

Опционально:
9. Возвращать архив фотографий пользователя за указанный период.

10. Искать фотографии польователя по указанному в поиске цвету.

11. Возвращать данные в зависимости от запроса в json или xml.
