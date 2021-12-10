from abc import ABC, abstractmethod


class Serializer(ABC):
    @abstractmethod
    def load(self, path):
        '''Load data from file with path "path" to python dictionary'''

    @abstractmethod
    def save(self, data, path):
        '''Save data to file with path "path"'''

    def check_file_extension(self, path, extension):
        '''Check if file with path "path" has specified extension'''
        if path.lower().endswith(extension):
            return True
        else:
            return False
