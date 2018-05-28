﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.core.Termin import Termin
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.person.internal.PersonAttrTerminType import PersonAttrTerminType
from pullenti.ner.person.internal.PersonAttrTerminType2 import PersonAttrTerminType2


class PersonAttrTermin(Termin):
    
    def __init__(self, v : str, lang_ : 'MorphLang'=MorphLang()) -> None:
        self.typ = PersonAttrTerminType.OTHER
        self.typ2 = PersonAttrTerminType2.UNDEFINED
        self.can_be_unique_identifier = False
        self.can_has_person_after = 0
        self.can_be_same_surname = False
        self.can_be_independant = False
        self.is_boss = False
        self.is_kin = False
        self.is_military_rank = False
        self.is_nation = False
        self.is_doubt = False
        super().__init__(None, lang_, False)
        self.init_by_normal_text(v, lang_)

    
    @staticmethod
    def _new2073(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'PersonAttrTerminType') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2102(_arg1 : str, _arg2 : 'PersonAttrTerminType') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.typ = _arg2
        return res
    
    @staticmethod
    def _new2104(_arg1 : str, _arg2 : 'PersonAttrTerminType', _arg3 : 'MorphGender') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.typ = _arg2
        res.gender = _arg3
        return res
    
    @staticmethod
    def _new2105(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'PersonAttrTerminType', _arg4 : 'MorphGender') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1, _arg2)
        res.typ = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new2113(_arg1 : str, _arg2 : str, _arg3 : 'PersonAttrTerminType2', _arg4 : 'PersonAttrTerminType') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.canonic_text = _arg2
        res.typ2 = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new2114(_arg1 : str, _arg2 : 'MorphLang', _arg3 : str, _arg4 : 'PersonAttrTerminType2', _arg5 : 'PersonAttrTerminType') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1, _arg2)
        res.canonic_text = _arg3
        res.typ2 = _arg4
        res.typ = _arg5
        return res
    
    @staticmethod
    def _new2119(_arg1 : str, _arg2 : 'PersonAttrTerminType2', _arg3 : 'PersonAttrTerminType') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.typ2 = _arg2
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2120(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'PersonAttrTerminType2', _arg4 : 'PersonAttrTerminType') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1, _arg2)
        res.typ2 = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new2139(_arg1 : str, _arg2 : str, _arg3 : 'PersonAttrTerminType', _arg4 : 'PersonAttrTerminType2') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.canonic_text = _arg2
        res.typ = _arg3
        res.typ2 = _arg4
        return res
    
    @staticmethod
    def _new2141(_arg1 : str, _arg2 : 'PersonAttrTerminType2', _arg3 : 'PersonAttrTerminType', _arg4 : 'MorphLang') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.typ2 = _arg2
        res.typ = _arg3
        res.lang = _arg4
        return res
    
    @staticmethod
    def _new2146(_arg1 : str, _arg2 : 'PersonAttrTerminType', _arg3 : 'MorphLang') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.typ = _arg2
        res.lang = _arg3
        return res