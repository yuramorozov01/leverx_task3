import os
import sys
from json import JSONDecodeError

import xmltodict

from exceptions.format_error import FormatError
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
        repository.create_views()


def save_instances_into_database(instances, repository):
    repository.add_many(instances)


def calculate_tasks(rooms_repository, students_repository):
    amount_of_students_in_rooms_tuple = students_repository.get_amount_of_students_in_rooms()
    amount_of_students_in_rooms_list_of_dicts = [
        {'room_id': key, 'amount_of_students': value} for key, value in amount_of_students_in_rooms_tuple
    ]

    top_5_rooms_min_avg_age_tuple = students_repository.get_top_5_rooms_min_avg_age()
    top_5_rooms_min_avg_age_list_of_dicts = [
        {'room_id': key, 'average_age': float(value)} for key, value in top_5_rooms_min_avg_age_tuple
    ]

    top_5_rooms_max_diff_in_age_tuple = students_repository.get_top_5_rooms_max_diff_in_age()
    top_5_rooms_max_diff_in_age_list_of_dicts = [
        {'room_id': key, 'diff_in_age': value} for key, value in top_5_rooms_max_diff_in_age_tuple
    ]

    list_of_rooms_with_different_sexes_tuple = students_repository.get_list_of_rooms_with_different_sexes()
    list_of_rooms_with_different_sexes_list = [item[0] for item in list_of_rooms_with_different_sexes_tuple]

    res = {
        'amount_of_students_in_rooms': amount_of_students_in_rooms_list_of_dicts,
        'top_5_rooms_min_avg_age': top_5_rooms_min_avg_age_list_of_dicts,
        'top_5_rooms_max_diff_in_age': top_5_rooms_max_diff_in_age_list_of_dicts,
        'list_of_rooms_with_different_sexes': list_of_rooms_with_different_sexes_list,
    }
    return res


def save_data(serializer, data, path):
    '''Save processed data with specified serializer to file with path "path"'''
    try:
        serializer.save(data, path)
    except (FileNotFoundError, FormatError, JSONDecodeError, xmltodict.expat.ExpatError) as e:
        sys.exit(str(e))