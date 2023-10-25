from datetime import datetime

from .response_parsers import ResponseParser
from . import types_parsers as tp


simple_parse_types = (int, float, str)
for type_ in simple_parse_types:
    ResponseParser.register_general_type_parser(type_, type_)

ResponseParser.register_general_type_parser(bytes, tp.bytes_parser)
ResponseParser.register_general_type_parser(datetime, tp.datetime_parser)
