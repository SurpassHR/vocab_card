from collections import namedtuple
from os import getcwd, path

ITEM = namedtuple('Item', ['id', 'text', 'source', 'target', 'service', 'result', 'timestamp'])
RESULT = namedtuple(
    'Result2',
    [
        'text', # str
        'region', # list
        'symbol', # list
        'meaning', # List[MEANING]
    ]
)
MEANING = namedtuple(
    'MEANING',
    [
        'mean', # str
        'trait', # str
        'explain', # str
        'exampleEn', # list
        'exampleZh', # list
    ]
)

CONFIG_FILE = path.abspath(path.join(getcwd(), 'config.yaml'))