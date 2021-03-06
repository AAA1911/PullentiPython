﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class MorphFinite(IntEnum):
    """ Это для английских глаголов """
    UNDEFINED = 0
    FINITE = 1
    INFINITIVE = 2
    PARTICIPLE = 4
    GERUND = 8
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)