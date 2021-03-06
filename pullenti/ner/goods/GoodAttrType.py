﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class GoodAttrType(IntEnum):
    """ Типы атрибутоа """
    UNDEFINED = 0
    KEYWORD = 1
    """ Ключевое слово (тип товара) """
    CHARACTER = 2
    """ Качественное свойство """
    PROPER = 3
    """ Собственное имя """
    MODEL = 4
    """ Модель """
    NUMERIC = 5
    """ Количественное свойство """
    REFERENT = 6
    """ Ссылка на некоторую сущность (страна, организация - производитель ...) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)