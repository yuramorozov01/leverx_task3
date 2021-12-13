import os
import sys
from json import JSONDecodeError

import xmltodict

from argument_parser import get_argument_parser
from exceptions.format_error import FormatError
from models.room import Room
from models.student import Student
from repositories.rooms_repository import RoomsRepository
from repositories.students_repository import StudentsRepository
from serializers.json_serializer import JsonSerializer
from serializers.xml_serializer import XmlSerializer


def get_file_extension(path):
    name, ext = os.path.splitext(path)
    if len(ext) >= 1:
        ext = ext[1:]
    return ext


def get_serializer_class(output_format):
    '''Determine serializer class by a data format.
    Can be 2 formats:
        - JSON
        - XML
    '''
    formats = {
        'json': JsonSerializer,
        'xml': XmlSerializer,
    }
    return formats.get(output_format)


def get_serializer_instance(format_):
    '''Getting instance of specified serializer class'''
    serializer_class = get_serializer_class(format_)
    if serializer_class is None:
        sys.exit(f'Unknown format: {format_}')
    serializer = serializer_class()
    return serializer


def get_instances_by_data(serializer, path, model):
    '''Loading data in dictionary format with specified serializer and from specified path.'''
    try:
        dict_data = serializer.load(path)
        return list(map(model, dict_data))
    except FileNotFoundError as e:
        sys.exit(f'Cannot find file {path}')
    except (FormatError, JSONDecodeError, xmltodict.expat.ExpatError) as e:
        sys.exit(str(e))


def configure_database(repositories):
    if len(repositories) > 0:
        repositories[0].create_database()

    for repository in repositories:
        repository.create_table()
        repository.create_indices()


def save_instances_into_database(instances, repository):
    repository.add_many(instances)


def calculate_tasks(rooms_repository, students_repository):
    amount_of_students_in_rooms_tuple = students_repository.get_amount_of_students_in_rooms()
    amount_of_students_in_rooms_list_of_dicts = [
        {'room_id': key, 'amount_of_students': value} for key, value in amount_of_students_in_rooms_tuple
    ]

    top_5_min_avg_age_tuple = students_repository.get_top_5_min_avg_age()
    top_5_min_avg_age_list_of_dicts = [
        {'room_id': key, 'average_age': float(value)} for key, value in top_5_min_avg_age_tuple
    ]

    res = {
        'amount_of_students_in_rooms': amount_of_students_in_rooms_list_of_dicts,
        'top_5_min_avg_age': top_5_min_avg_age_list_of_dicts,
    }
    return res


def save_data(serializer, data, path):
    '''Save processed data with specified serializer to file with path "path"'''
    try:
        serializer.save(data, path)
    except (FileNotFoundError, FormatError, JSONDecodeError, xmltodict.expat.ExpatError) as e:
        sys.exit(str(e))


if __name__ == '__main__':
    # Parse console arguments
    parser = get_argument_parser()
    args = parser.parse_args()

    path_to_students = args.students
    path_to_rooms = args.rooms
    format_ = args.format
    path_to_save = args.output

    # Get serializers for every file by a format
    serializer_to_load_students = get_serializer_instance(get_file_extension(path_to_students))
    serializer_to_load_rooms = get_serializer_instance(get_file_extension(path_to_rooms))
    serializer_to_save = get_serializer_instance(format_)

    # Create instances of students and rooms with received serializers
    rooms_instances = get_instances_by_data(serializer_to_load_rooms, path_to_rooms, Room)
    students_instances = get_instances_by_data(serializer_to_load_students, path_to_students, Student)

    # Configure database
    configure_database((RoomsRepository, StudentsRepository))

    # Save instances into database
    save_instances_into_database(rooms_instances, RoomsRepository)
    save_instances_into_database(students_instances, StudentsRepository)

    data = calculate_tasks(RoomsRepository, StudentsRepository)

    # Save result into a specified file
    save_data(serializer_to_save, data, path_to_save)
    print(f'File has been successfully saved to {path_to_save}')

    RoomsRepository.close_connection()
