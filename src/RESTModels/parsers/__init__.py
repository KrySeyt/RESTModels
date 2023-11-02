from datetime import datetime, date, time, timedelta

from .type_alias_parsers import TypeAliasParser
from . import type_alias_parsers as tp


TypeAliasParser.register_general_alias_parser(int, tp.int_alias_parser)
TypeAliasParser.register_general_alias_parser(bool, tp.bool_alias_parser)
TypeAliasParser.register_general_alias_parser(float, tp.float_alias_parser)
TypeAliasParser.register_general_alias_parser(str, tp.str_alias_parser)
TypeAliasParser.register_general_alias_parser(bytes, tp.bytes_alias_parser)
TypeAliasParser.register_general_alias_parser(datetime, tp.datetime_alias_parser)
TypeAliasParser.register_general_alias_parser(date, tp.date_alias_parser)
TypeAliasParser.register_general_alias_parser(time, tp.time_alias_parser)
TypeAliasParser.register_general_alias_parser(timedelta, tp.timedelta_alias_parser)
TypeAliasParser.register_general_alias_parser(tuple, tp.tuple_alias_parser)
TypeAliasParser.register_general_alias_parser(list, tp.list_alias_parser)
TypeAliasParser.register_general_alias_parser(set, tp.set_alias_parser)
TypeAliasParser.register_general_alias_parser(frozenset, tp.frozenset_alias_parser)
