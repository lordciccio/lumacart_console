import csv
import chardet 

DATA_FORMAT_CSV = 'CSV'

def get_reader(format):
    return {
        DATA_FORMAT_CSV: CSVReader
    }[format]

class Reader(object):
    
    def parse_doc(self, doc_data):
        raise NotImplementedError
    
    def get_header(self):
        raise NotImplementedError
    
    def iter_doc(self):
        raise NotImplementedError

class EncodingDetectionError(Exception):
    pass
    
def get_encoding(path):
    with open(path, 'rb') as f:
        raw_content = f.read()
        
        """ dovremmo includere la ricerca con BOM character e in quel caso va tolto dai bytes
        BOM_encoding_map = (('\xef\xbb\xbf', 'utf-8'), ('\xff\xfe\0\0', 'utf-32'), ('\0\0\xfe\xff', 'UTF-32BE'), ('\xff\xfe', 'utf-16'), ('\xfe\xff', 'UTF-16BE'))

        for bom, encoding in BOM_encoding_map:
            if bytes.startswith(bom):
                return bytes[len(bom):], encoding
        """
        det = chardet.detect(raw_content)
        encoding = det['encoding']
        confidence = det['confidence']
        if not encoding or confidence < 1.0:
            for option in ["UTF-8", "windows-1252", "iso-8859-1", "UTF-16"]:
                try:
                    raw_content.decode(option)
                except:
                    continue
                else:
                    encoding = option
                    break
        if not encoding:
            raise EncodingDetectionError("Unable to detect encoding for %s" % path)
        return encoding

REMOVE_CTRL_CHARS = [
    chr(26) # SUB (1A)
]

class CSVReader(Reader):
    
    def __init__(self, headers = None, delimiter = ',', **kwargs):
        self.csv_headers = headers
        self.real_headers = {}
        self.delimiter = delimiter
        
    def _column_name(self, key):
        return key.strip()
    
    def remove_control_characters(self, s):
        new_str = ""
        for c in s:
            if c not in REMOVE_CTRL_CHARS:
                new_str = new_str + c
        return new_str
    
    def _decode_record(self, record):
        result = {}
        for k, v in record.items():
            if k is None or k.strip() == '':
                continue
            if v is None: v = ''
            result[self._column_name(k)] = self.remove_control_characters(v)
        return result
    
    def get_header(self):
        return self.reader.fieldnames
    
    def parse_doc(self, doc_data):
        csv_parameters = {
            'delimiter': self.delimiter,
        }
        if self.csv_headers:
            csv_parameters['fieldnames'] = self.csv_headers
        self.reader = csv.DictReader(doc_data, **csv_parameters)

    def iter_doc(self):
        for r in self.reader:
            yield self._decode_record(r)
