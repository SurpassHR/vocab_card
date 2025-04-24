import os
import sys
from collections import namedtuple

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

try:
    _ = sys._MEIPASS
    CONFIG_FILE = os.path.join(os.getcwd(), 'config.yaml')
except:
    CONFIG_FILE = os.path.join(os.getcwd(), '..', 'config', 'config.yaml')