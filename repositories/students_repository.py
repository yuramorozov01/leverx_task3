from repositories.repository import Repository


class StudentsRepository(Repository):
    _connection = Repository.get_connection()

    @classmethod
    def create_table(cls):
        if cls._connection is not None:
            query = (
                "CREATE TABLE IF NOT EXISTS `students` ("
                "   `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,"
                "   `name` VARCHAR(256) NOT NULL,"
                "   `birthday` DATE NOT NULL,"
                "   `sex` enum('M','F') NOT NULL,"
                "   `room` INT(11) UNSIGNED," 
                "   PRIMARY KEY (`id`),"
                "   CONSTRAINT `students_room_fk` FOREIGN KEY (`room`) "
                "       REFERENCES `rooms` (`id`) ON UPDATE CASCADE ON DELETE SET NULL"
                ") ENGINE=InnoDB"
            )
            cls.make_query(query)

    @classmethod
    def add(cls, student):
        if cls._connection is not None:
            query = (
                "REPLACE INTO `students` (id, name, birthday, sex, room) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            params = (
                student.id,
                student.name,
                student.birthday,
                student.sex,
                student.room,
            )
            cls.make_query(query, params)

    @classmethod
    def add_many(cls, students):
        if cls._connection is not None:
            query = (
                "REPLACE INTO `students` (id, name, birthday, sex, room) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            params = [(student.id, student.name, student.birthday, student.sex, student.room) for student in students]
            cls.make_many_query(query, params)

