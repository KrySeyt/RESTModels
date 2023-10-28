from datetime import datetime

from .type_alias_parsers import TypeAliasParser
from . import type_alias_parsers as tp


TypeAliasParser.register_general_type_parser(int, tp.int_alias_parser)
TypeAliasParser.register_general_type_parser(float, tp.float_alias_parser)
TypeAliasParser.register_general_type_parser(str, tp.str_alias_parser)
TypeAliasParser.register_general_type_parser(bytes, tp.bytes_alias_parser)
TypeAliasParser.register_general_type_parser(datetime, tp.datetime_alias_parser)
TypeAliasParser.register_general_type_parser(tuple, tp.tuple_alias_parser)
TypeAliasParser.register_general_type_parser(list, tp.list_alias_parser)
