import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_user_by_id(self, user_id):
        """ Получаем пользователя по ID """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM botusers where id = ?', (user_id,)).fetchall()
            return result

    def add_user(self, user_id, c_name, c_fname, c_lname, c_lang, c_tel, d_date):
        """ Добавляем нового пользователя """
        with self.connection:
            result = self.cursor.execute('INSERT INTO botusers VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, c_name, c_fname, c_lname, c_lang, c_tel, d_date,))
            return result

    def select_pref_by_userid(self, user_id):
        """ Получаем сохраненные пользовательские настройки """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM userpref WHERE user_id = ?', (user_id,)).fetchall()
            return result

    def add_userpref(self, uid, cityname, citycountry, cityid, mtime, etime, ddate):
        """ Добавить пользовательские настройки """
        with self.connection:
            result = self.cursor.execute('INSERT INTO userpref VALUES (?, ?, ?, ?, ?, ?, ?)', (uid, cityname, citycountry, cityid, mtime, etime, ddate,))
            return result

    def update_userpref(self):
        """ Изменение пользовательских настроек """
        return None

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()