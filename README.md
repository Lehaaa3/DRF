Django Rest Framework HW-s

Для работы с проектом:

1. Заполните файл .env по примеру .env.example
2. Установите зависимости из файла requirements.txt
3. Примените миграции
4. Примените команду python manage.py cities_light для заполнения таблицы с городами (Может занять некоторое время. Не
   обязательно, если хотите оставить поле city в таблице users_user равным null)
5. Заполните таблицы используя фикстуры:
   python manage.py loaddata users_fixture.json
   python manage.py loaddata courses_fixture.json
   python manage.py loaddata lessons_fixture.json
   python manage.py loaddata payments_fixture.json
   python manage.py loaddata groups_fixture.json
   

