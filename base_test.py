import pymysql
from config import *


class Mysql:
    def connect(): #вопрос, сюда он просит передать аргумент Self, ты говорил что без него работать не будет - но работает. Какие последствия?
        try:
            connection = pymysql.connect(
            host = host,
            port = 3306,
            user = user,
            password = password,
            database = db_name,
            cursorclass = pymysql.cursors.DictCursor
            )
            print("Подключились, все збс")
            return connection

        except Exception as ex:
            print("Не подключились, ошибка", ex)

    def add_employe():
        # user_name = input('Имя пользователя')
        # ms_id = input('Учетка в МС')
        # systems_id = input('Айди пакета бонусов')
        connection = Mysql.connect()
        print(connection)
        with connection.cursor as cursor:
            insert_query = "INSERT INTO `employes` (user_name) VALUES ('admin');"
            cursor.execute(insert_query)
            connection.commit()





Mysql.add_employe()

#add_employe(user_name=1,ms_id=2,systems_id=3)
