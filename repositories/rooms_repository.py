from repositories.repository import Repository


class RoomsRepository(Repository):
    _connection = Repository.get_connection()

    @classmethod
    def create_rooms_table(cls):
        if cls._connection is not None:
            query = (
                "CREATE TABLE IF NOT EXISTS `rooms` ("
                "   `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,"
                "   `name` VARCHAR(256) NOT NULL,"
                "   PRIMARY KEY (`id`)"
                ") ENGINE=InnoDB"
            )
            cls.make_query(query)

    @classmethod
    def add_room(cls, room):
        if cls._connection is not None:
            query = (
                "INSERT INTO `rooms` (id, name) "
                "VALUES (%s, %s)"
            )
            params = (room.id, room.name)
            cls.make_query(query, params)
