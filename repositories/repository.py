from abc import ABC, abstractmethod

import pymysql.cursors
from decouple import config


class Repository(ABC):
    _connection = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            try:
                cnx = pymysql.connect(
                    user=config('DB_USER'),
                    password=config('DB_PASSWORD'),
                    host=config('DB_HOST'),
                    port=config('DB_PORT', default=3306, cast=int)
                )
                cls._connection = cnx
            except pymysql.Error as err:
                print(err)
                cls.close_connection()
        return cls._connection

    @classmethod
    def close_connection(cls):
        if cls._connection is not None:
            try:
                cls._connection.close()
                cls._connection = None
            except pymysql.Error as err:
                print(err)
                cls.close_connection()

    @classmethod
    def make_query(cls, query, params=None):
        if cls._connection is not None:
            try:
                cursor = cls._connection.cursor()
                cursor.execute(query, params)
                cls._connection.commit()
                result = cursor.fetchall()
                cursor.close()
                return result
            except pymysql.Error as err:
                print(err)

    @classmethod
    def make_many_query(cls, query, list_params=None):
        if cls._connection is not None:
            try:
                cursor = cls._connection.cursor()
                cursor.executemany(query, list_params)
                cls._connection.commit()
                cursor.close()
            except pymysql.Error as err:
                print(err)

    @classmethod
    def create_database(cls):
        query = """
            CREATE DATABASE IF NOT EXISTS {} 
            DEFAULT CHARACTER SET utf8 
            DEFAULT COLLATE utf8_general_ci;
        """.format(config('DB_NAME'))
        cls.make_query(query)

        query = """
            USE {}
        """.format(config('DB_NAME'))
        cls.make_query(query)

        query = """
            SET sql_mode='NO_AUTO_VALUE_ON_ZERO'
        """
        cls.make_query(query)

        cls._create_stored_procedures()

    @classmethod
    def _create_stored_procedures(cls):
        query = """
            DROP PROCEDURE IF EXISTS create_index; 
        """
        cls.make_query(query)

        query = """
            CREATE PROCEDURE create_index(
                current_database VARCHAR(256),
                index_name_ VARCHAR(256),
                table_name_ VARCHAR(256),
                columns_ VARCHAR(256)
            ) 
            BEGIN
                DECLARE is_exists INTEGER DEFAULT 0; 
                SELECT COUNT(1) INTO is_exists
                FROM INFORMATION_SCHEMA.STATISTICS 
                WHERE TABLE_SCHEMA=current_database 
                      AND TABLE_NAME=table_name_
                      AND INDEX_NAME=index_name_;
                IF is_exists = 0 THEN
                    SET @query_ = CONCAT('CREATE INDEX ', index_name_, ' ON ', table_name_, ' (', columns_, ')');
                    PREPARE stmt FROM @query_;
                    EXECUTE stmt;
                    DEALLOCATE PREPARE stmt;
                END IF;
            END; 
        """
        cls.make_query(query)

        query = """
            DROP PROCEDURE IF EXISTS get_amount_of_students_in_rooms; 
        """
        cls.make_query(query)

        query = """
            CREATE PROCEDURE get_amount_of_students_in_rooms()
            BEGIN
                SELECT `room`, COUNT(*) as `amount_of_students`
                FROM `students`
                GROUP BY `room`;
            END;
        """
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

    @classmethod
    @abstractmethod
    def create_indices(cls):
        '''Create specified indices in the table'''

    @classmethod
    @abstractmethod
    def create_views(cls):
        '''Create views with specified table'''
