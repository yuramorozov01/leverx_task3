from repositories.repository import Repository


class RoomsRepository(Repository):
    _connection = Repository.get_connection()

    @classmethod
    def create_table(cls):
        query = """
            CREATE TABLE IF NOT EXISTS `rooms` (
               `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
               `name` VARCHAR(256) NOT NULL,
               PRIMARY KEY (`id`)
            ) ENGINE=InnoDB
        """
        cls.make_query(query)

    @classmethod
    def add(cls, room):
        query = """
            REPLACE INTO `rooms` (id, name)
            VALUES (%s, %s)
        """
        params = (room.id, room.name)
        cls.make_query(query, params)

    @classmethod
    def add_many(cls, rooms):
        query = """
            REPLACE INTO `rooms` (id, name) 
            VALUES (%s, %s)
        """
        params = [(room.id, room.name) for room in rooms]
        cls.make_many_query(query, params)

    @classmethod
    def create_indices(cls):
        pass
