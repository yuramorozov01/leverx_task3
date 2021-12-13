from repositories.repository import Repository


class StudentsRepository(Repository):
    _connection = Repository.get_connection()

    @classmethod
    def create_table(cls):
        query = """
            CREATE TABLE IF NOT EXISTS `students` (
               `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
               `name` VARCHAR(256) NOT NULL,
               `birthday` DATE NOT NULL,
               `sex` enum('M','F') NOT NULL,
               `room` INT(11) UNSIGNED,
               PRIMARY KEY (`id`),
               CONSTRAINT `students_room_fk` FOREIGN KEY (`room`) 
                   REFERENCES `rooms` (`id`) ON UPDATE CASCADE ON DELETE SET NULL
            ) ENGINE=InnoDB
        """
        cls.make_query(query)

    @classmethod
    def add(cls, student):
        query = """
            REPLACE INTO `students` (id, name, birthday, sex, room) 
            VALUES (%s, %s, %s, %s, %s)
        """
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
        query = """
            REPLACE INTO `students` (id, name, birthday, sex, room) 
            VALUES (%s, %s, %s, %s, %s)
        """
        params = [(student.id, student.name, student.birthday, student.sex, student.room) for student in students]
        cls.make_many_query(query, params)

    @classmethod
    def create_indices(cls):
        query = """
            CALL create_index(DATABASE(), 'idx_students_name', 'students', 'name')
        """
        cls.make_query(query)

    @classmethod
    def get_amount_of_students_in_rooms(cls):
        query = """
            CALL get_amount_of_students_in_rooms()
        """
        return cls.make_query(query)

    @classmethod
    def get_top_5_min_avg_age(cls):
        query = """
            SELECT * FROM `top_5_min_avg_age`;
        """
        return cls.make_query(query)
