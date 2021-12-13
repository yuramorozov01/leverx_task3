import utils
from argument_parser import get_argument_parser
from models.room import Room
from models.student import Student
from repositories.rooms_repository import RoomsRepository
from repositories.students_repository import StudentsRepository

if __name__ == '__main__':
    # Parse console arguments
    parser = get_argument_parser()
    args = parser.parse_args()

    path_to_students = args.students
    path_to_rooms = args.rooms
    format_ = args.format
    path_to_save = args.output

    # Get serializers for every file by a format
    serializer_to_load_students = utils.get_serializer_instance(utils.get_file_extension(path_to_students))
    serializer_to_load_rooms = utils.get_serializer_instance(utils.get_file_extension(path_to_rooms))
    serializer_to_save = utils.get_serializer_instance(format_)

    # Create instances of students and rooms with received serializers
    rooms_instances = utils.get_instances_by_data(serializer_to_load_rooms, path_to_rooms, Room)
    students_instances = utils.get_instances_by_data(serializer_to_load_students, path_to_students, Student)

    # Configure database
    utils.configure_database((RoomsRepository, StudentsRepository))

    # Save instances into database
    utils.save_instances_into_database(rooms_instances, RoomsRepository)
    utils.save_instances_into_database(students_instances, StudentsRepository)

    data = utils.calculate_tasks(RoomsRepository, StudentsRepository)

    # Save result into a specified file
    utils.save_data(serializer_to_save, data, path_to_save)
    print(f'File has been successfully saved to {path_to_save}')

    RoomsRepository.close_connection()
