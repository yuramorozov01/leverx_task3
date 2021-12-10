import os
import sys
from json import JSONDecodeError

import xmltodict

from argument_parser import get_argument_parser
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


def get_dict_of_data(serializer, path):
    '''Loading data in dictionary format with specified serializer and from specified path.'''
    try:
        dict_data = serializer.load(path)
        return dict_data
    except FileNotFoundError as e:
        sys.exit(f'Cannot find file {path}')
    except (FormatError, JSONDecodeError, xmltodict.expat.ExpatError) as e:
        sys.exit(str(e))


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

    # Load students and rooms into dictionaries with received serializers
    dict_students = get_dict_of_data(serializer_to_load_students, path_to_students)
    dict_rooms = get_dict_of_data(serializer_to_load_rooms, path_to_rooms)

    # Save data into a specified file
    # data = []
    # save_data(serializer_to_save, data, path_to_save)
    # print(f'File has been successfully saved to {path_to_save}')
