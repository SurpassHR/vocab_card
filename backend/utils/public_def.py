from collections import namedtuple

ITEM = namedtuple('Item', ['id', 'text', 'source', 'target', 'service', 'result', 'timestamp'])
RESULT = namedtuple('Result', ['text', 'region', 'symbol', 'trait', 'meaning', 'explain', 'exampleZh', 'exampleEn'])

RESULT_2 = namedtuple(
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