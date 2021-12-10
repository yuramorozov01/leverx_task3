import json

from exceptions.format_error import FormatError
from serializers.serializer import Serializer


class JsonSerializer(Serializer):
    def load(self, path):
        if self.check_file_extension(path, '.json'):
            json_data = None
            with open(path, 'r') as f:
                json_data = json.load(f)
            return json_data
        else:
            raise FormatError('File extensions is not ".json"')

    def save(self, data, path):
        if self.check_file_extension(path, '.json'):
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)
        else:
            raise FormatError('File extensions is not ".json"')
