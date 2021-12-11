from decouple import config
import mysql.connector


class Repository:
    _connection = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            try:
                cnx = mysql.connector.connect(
                    user=config('DB_USER'),
                    password=config('DB_PASSWORD'),
                    host=config('DB_HOST'),
                    database=config('DB_NAME')
                )
                cls._connection = cnx
            except mysql.connector.Error as err:
                print(err.msg)
                cls._close_connection()
        return cls._connection

    @classmethod
    def _close_connection(cls):
        if cls._connection is not None:
            try:
                cls._connection.close()
                cls._connection = None
            except mysql.connector.Error as err:
                print(err.msg)
                cls._close_connection()

    @classmethod
    def make_query(cls, query, params=None):
        if cls._connection is not None:
            try:
                cursor = cls._connection.cursor()
                cursor.execute(query, params)
                cls._connection.commit()
            except mysql.connector.Error as err:
                print(err.msg)

    @classmethod
    def _create_database(cls):
        if cls._connection is not None:
            query = (
                "CREATE DATABASE %s DEFAULT CHARACTER SET 'utf8'"
            )
            params = (config('DB_NAME'),)
            cls.make_query(query, params)
