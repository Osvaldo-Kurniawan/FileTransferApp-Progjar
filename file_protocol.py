import json
import logging
import shlex

from file_interface import FileInterface

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def proses_string(self, string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk}")
        c = shlex.split(string_datamasuk)
        try:
            c_request = c[0].strip().lower()
            logging.warning(f"memproses request: {c_request}")
            params = c[1:]
            if c_request == 'upload':
                filename = params[0]
                encoded_file = ' '.join(params[1:])
                params = [filename, encoded_file]
            cl = getattr(self.file, c_request)(params)
            return json.dumps(cl)
        except Exception as e:
            return json.dumps(dict(status='ERROR', data=f'request tidak dikenali: {str(e)}'))

if __name__ == '__main__':
    fp = FileProtocol()