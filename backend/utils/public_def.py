from collections import namedtuple

ITEM = namedtuple('Item', ['id', 'text', 'source', 'target', 'service', 'result', 'timestamp'])
RESULT = namedtuple('Result', ['text', 'region', 'symbol', 'trait', 'meaning', 'explain', 'exampleZh', 'exampleEn'])