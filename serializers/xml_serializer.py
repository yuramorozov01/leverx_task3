import xmltodict

from exceptions.format_error import FormatError
from serializers.serializer import Serializer


class XmlSerializer(Serializer):
    def load(self, path):
        if self.check_file_extension(path, '.xml'):
            xml_data = None
            with open(path, 'r') as f:
                xml_data = xmltodict.parse(f.read())
            return xml_data
        else:
            raise FormatError('File extensions is not ".xml"')

    def save(self, data, path):
        if self.check_file_extension(path, '.xml'):
            with open(path, 'w') as f:
                to_save = data
                if isinstance(data, list):
                    to_save = {'root': {'room': data}}
                xmltodict.unparse(to_save, output=f, pretty=True, full_document=False)
        else:
            raise FormatError('File extensions is not ".xml"')
