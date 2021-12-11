from abc import ABC, abstractmethod

import mysql.connector
from decouple import config


class Repository(ABC):
    _connection = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            try:
                cnx = mysql.connector.connect(
                    user=config('DB_USER'),
                    password=config('DB_PASSWORD'),
                    host=config('DB_HOST'),
                    port=config('DB_PORT'),
                    auth_plugin='mysql_native_password'
                )
                cls._connection = cnx
            except mysql.connector.Error as err:
                print(err.msg)
                cls.close_connection()
        return cls._connection

    @classmethod
    def close_connection(cls):
        if cls._connection is not None:
            try:
                cls._connection.close()
                cls._connection = None
            except mysql.connector.Error as err:
                print(err.msg)
                cls.close_connection()

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
    def make_many_query(cls, query, list_params=None):
        if cls._connection is not None:
            try:
                cursor = cls._connection.cursor()
                cursor.executemany(query, list_params)
                cls._connection.commit()
            except mysql.connector.Error as err:
                print(err.msg)

    @classmethod
    def create_database(cls):
        if cls._connection is not None:
            query = (
                "CREATE DATABASE IF NOT EXISTS {} "
                "DEFAULT CHARACTER SET utf8 "
                "DEFAULT COLLATE utf8_general_ci;"
            ).format(config('DB_NAME'))
            cls.make_query(query)

            query = (
                "USE {}"
            ).format(config('DB_NAME'))
            cls.make_query(query)

            query = (
                "SET sql_mode='NO_AUTO_VALUE_ON_ZERO'"
            )
            cls.make_query(query)

    @classmethod
    @abstractmethod
    def create_table(cls):
        '''Create table in database for specified model'''

    @classmethod
    @abstractmethod
    def add(cls, instance):
        '''Add instance to database'''

    @classmethod
    @abstractmethod
    def add_many(cls, instances):
        '''Add list of instances to database'''
