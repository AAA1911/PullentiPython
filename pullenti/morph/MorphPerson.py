﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class MorphPerson(IntEnum):
    """ Лицо (1, 2, 3) """
    UNDEFINED = 0
    """ Неопределено """
    FIRST = 1
    """ Первое """
    SECOND = 2
    """ Второе """
    THIRD = 4
    """ Третье """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)