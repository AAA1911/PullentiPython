﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.Referent import Referent
from pullenti.ner.instrument.InstrumentKind import InstrumentKind



class InstrumentBlockReferent(Referent):
    """ Представление нормативно-правового документа или его части """
    
    def __init__(self, typename : str=None) -> None:
        from pullenti.ner.instrument.internal.MetaInstrumentBlock import MetaInstrumentBlock
        self.__m_children = None
        super().__init__(Utils.ifNotNull(typename, InstrumentBlockReferent.OBJ_TYPENAME))
        self.instance_of = MetaInstrumentBlock.GLOBAL_META
    
    OBJ_TYPENAME = "INSTRBLOCK"
    
    ATTR_KIND = "KIND"
    
    ATTR_KIND2 = "KIND_SEC"
    
    ATTR_CHILD = "CHILD"
    
    ATTR_VALUE = "VALUE"
    
    ATTR_REF = "REF"
    
    ATTR_EXPIRED = "EXPIRED"
    
    ATTR_NAME = "NAME"
    
    ATTR_NUMBER = "NUMBER"
    
    ATTR_MINNUMBER = "MINNUMBER"
    
    ATTR_SUBNUMBER = "ADDNUMBER"
    
    ATTR_SUB2NUMBER = "ADDSECNUMBER"
    
    ATTR_SUB3NUMBER = "ADDTHIRDNUMBER"
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        from pullenti.ner.instrument.internal.MetaInstrumentBlock import MetaInstrumentBlock
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        res = Utils.newStringIO(None)
        ki = self.kind
        str0 = (MetaInstrumentBlock.GLOBAL_META.kind_feature.convert_inner_value_to_outer_value(Utils.enumToString(ki), lang) if isinstance(MetaInstrumentBlock.GLOBAL_META.kind_feature.convert_inner_value_to_outer_value(Utils.enumToString(ki), lang), str) else None)
        if (str0 is not None): 
            print(str0, end="", file=res)
            if (self.kind2 != InstrumentKind.UNDEFINED): 
                str0 = (MetaInstrumentBlock.GLOBAL_META.kind_feature.convert_inner_value_to_outer_value(Utils.enumToString(self.kind2), lang) if isinstance(MetaInstrumentBlock.GLOBAL_META.kind_feature.convert_inner_value_to_outer_value(Utils.enumToString(self.kind2), lang), str) else None)
                if (str0 is not None): 
                    print(" ({0})".format(str0), end="", file=res, flush=True)
        if (self.number > 0): 
            if (ki == InstrumentKind.TABLE): 
                print(" {0} строк, {1} столбцов".format(len(self.children), self.number), end="", file=res, flush=True)
            else: 
                print(" №{0}".format(self.number), end="", file=res, flush=True)
                if (self.sub_number > 0): 
                    print(".{0}".format(self.sub_number), end="", file=res, flush=True)
                    if (self.sub_number2 > 0): 
                        print(".{0}".format(self.sub_number2), end="", file=res, flush=True)
                        if (self.sub_number3 > 0): 
                            print(".{0}".format(self.sub_number3), end="", file=res, flush=True)
                if (self.min_number > 0): 
                    for i in range(res.tell() - 1, -1, -1):
                        if (Utils.getCharAtStringIO(res, i) == ' ' or Utils.getCharAtStringIO(res, i) == '.'): 
                            Utils.insertStringIO(res, i + 1, "{0}-".format(self.min_number))
                            break
        ignore_ref = False
        if (self.is_expired): 
            print(" (утратить силу)", end="", file=res)
            ignore_ref = True
        elif (ki != InstrumentKind.EDITIONS and ki != InstrumentKind.APPROVED and isinstance(self.ref, DecreeReferent)): 
            print(" (*)", end="", file=res)
            ignore_ref = True
        str0 = self.get_string_value(InstrumentBlockReferent.ATTR_NAME)
        if ((str0) is None): 
            str0 = self.get_string_value(InstrumentBlockReferent.ATTR_VALUE)
        if (str0 is not None): 
            if (len(str0) > 100): 
                str0 = (str0[0 : 100] + "...")
            print(" \"{0}\"".format(str0), end="", file=res, flush=True)
        elif (not ignore_ref and isinstance(self.ref, Referent) and (lev < 30)): 
            print(" \"{0}\"".format(self.ref.to_string(short_variant, lang, lev + 1)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    @property
    def kind(self) -> 'InstrumentKind':
        """ Классификатор """
        s = self.get_string_value(InstrumentBlockReferent.ATTR_KIND)
        if (s is None): 
            return InstrumentKind.UNDEFINED
        try: 
            if (s == "Part" or s == "Base" or s == "Special"): 
                return InstrumentKind.UNDEFINED
            res = Utils.valToEnum(s, InstrumentKind)
            if (isinstance(res, InstrumentKind)): 
                return Utils.valToEnum(res, InstrumentKind)
        except Exception as ex1413: 
            pass
        return InstrumentKind.UNDEFINED
    
    @kind.setter
    def kind(self, value_) -> 'InstrumentKind':
        if (value_ != InstrumentKind.UNDEFINED): 
            self.add_slot(InstrumentBlockReferent.ATTR_KIND, Utils.enumToString(value_).upper(), True, 0)
        return value_
    
    @property
    def kind2(self) -> 'InstrumentKind':
        """ Классификатор дополнительный """
        s = self.get_string_value(InstrumentBlockReferent.ATTR_KIND2)
        if (s is None): 
            return InstrumentKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, InstrumentKind)
            if (isinstance(res, InstrumentKind)): 
                return Utils.valToEnum(res, InstrumentKind)
        except Exception as ex1414: 
            pass
        return InstrumentKind.UNDEFINED
    
    @kind2.setter
    def kind2(self, value_) -> 'InstrumentKind':
        if (value_ != InstrumentKind.UNDEFINED): 
            self.add_slot(InstrumentBlockReferent.ATTR_KIND2, Utils.enumToString(value_).upper(), True, 0)
        return value_
    
    @property
    def value(self) -> str:
        """ Значение """
        return self.get_string_value(InstrumentBlockReferent.ATTR_VALUE)
    
    @value.setter
    def value(self, value_) -> str:
        self.add_slot(InstrumentBlockReferent.ATTR_VALUE, value_, True, 0)
        return value_
    
    @property
    def ref(self) -> 'Referent':
        return (self.get_value(InstrumentBlockReferent.ATTR_REF) if isinstance(self.get_value(InstrumentBlockReferent.ATTR_REF), Referent) else None)
    
    @property
    def is_expired(self) -> bool:
        return self.get_string_value(InstrumentBlockReferent.ATTR_EXPIRED) == "true"
    
    @is_expired.setter
    def is_expired(self, value_) -> bool:
        self.add_slot(InstrumentBlockReferent.ATTR_EXPIRED, ("true" if value_ else None), True, 0)
        return value_
    
    @property
    def number(self) -> int:
        """ Номер (для диапазона - максимальный номер) """
        str0 = self.get_string_value(InstrumentBlockReferent.ATTR_NUMBER)
        if (str0 is None): 
            return 0
        inoutarg1415 = RefOutArgWrapper(None)
        inoutres1416 = Utils.tryParseInt(str0, inoutarg1415)
        i = inoutarg1415.value
        if (inoutres1416): 
            return i
        return 0
    
    @number.setter
    def number(self, value_) -> int:
        self.add_slot(InstrumentBlockReferent.ATTR_NUMBER, str(value_), True, 0)
        return value_
    
    @property
    def sub_number(self) -> int:
        """ Дополнительный номер (через точку за основным) """
        str0 = self.get_string_value(InstrumentBlockReferent.ATTR_SUBNUMBER)
        if (str0 is None): 
            return 0
        inoutarg1417 = RefOutArgWrapper(None)
        inoutres1418 = Utils.tryParseInt(str0, inoutarg1417)
        i = inoutarg1417.value
        if (inoutres1418): 
            return i
        return 0
    
    @sub_number.setter
    def sub_number(self, value_) -> int:
        self.add_slot(InstrumentBlockReferent.ATTR_SUBNUMBER, str(value_), True, 0)
        return value_
    
    @property
    def sub_number2(self) -> int:
        """ Дополнительный второй номер (через точку за дополнительным) """
        str0 = self.get_string_value(InstrumentBlockReferent.ATTR_SUB2NUMBER)
        if (str0 is None): 
            return 0
        inoutarg1419 = RefOutArgWrapper(None)
        inoutres1420 = Utils.tryParseInt(str0, inoutarg1419)
        i = inoutarg1419.value
        if (inoutres1420): 
            return i
        return 0
    
    @sub_number2.setter
    def sub_number2(self, value_) -> int:
        self.add_slot(InstrumentBlockReferent.ATTR_SUB2NUMBER, str(value_), True, 0)
        return value_
    
    @property
    def sub_number3(self) -> int:
        """ Дополнительный третий номер (через точку за вторым дополнительным) """
        str0 = self.get_string_value(InstrumentBlockReferent.ATTR_SUB3NUMBER)
        if (str0 is None): 
            return 0
        inoutarg1421 = RefOutArgWrapper(None)
        inoutres1422 = Utils.tryParseInt(str0, inoutarg1421)
        i = inoutarg1421.value
        if (inoutres1422): 
            return i
        return 0
    
    @sub_number3.setter
    def sub_number3(self, value_) -> int:
        self.add_slot(InstrumentBlockReferent.ATTR_SUB3NUMBER, str(value_), True, 0)
        return value_
    
    @property
    def min_number(self) -> int:
        """ Минимальный номер, если задан диапазон """
        str0 = self.get_string_value(InstrumentBlockReferent.ATTR_MINNUMBER)
        if (str0 is None): 
            return 0
        inoutarg1423 = RefOutArgWrapper(None)
        inoutres1424 = Utils.tryParseInt(str0, inoutarg1423)
        i = inoutarg1423.value
        if (inoutres1424): 
            return i
        return 0
    
    @min_number.setter
    def min_number(self, value_) -> int:
        self.add_slot(InstrumentBlockReferent.ATTR_MINNUMBER, str(value_), True, 0)
        return value_
    
    @property
    def name(self) -> str:
        """ Наименование """
        return self.get_string_value(InstrumentBlockReferent.ATTR_NAME)
    
    @name.setter
    def name(self, value_) -> str:
        self.add_slot(InstrumentBlockReferent.ATTR_NAME, value_, True, 0)
        return value_
    
    @property
    def children(self) -> typing.List['InstrumentBlockReferent']:
        """ Внутреннее содержимое """
        if (self.__m_children is None): 
            self.__m_children = list()
            for s in self.slots: 
                if (s.type_name == InstrumentBlockReferent.ATTR_CHILD): 
                    if (isinstance(s.value, InstrumentBlockReferent)): 
                        self.__m_children.append(s.value if isinstance(s.value, InstrumentBlockReferent) else None)
        return self.__m_children
    
    def add_slot(self, attr_name : str, attr_value : object, clear_old_value : bool, stat_count : int=0) -> 'Slot':
        self.__m_children = None
        return super().add_slot(attr_name, attr_value, clear_old_value, stat_count)
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        return obj == self
    
    @staticmethod
    def kind_to_rus_string(typ : 'InstrumentKind', short_val : bool) -> str:
        if (typ == InstrumentKind.APPENDIX): 
            return ("прил." if short_val else "Приложение")
        if (typ == InstrumentKind.CLAUSE): 
            return ("ст." if short_val else "Статья")
        if (typ == InstrumentKind.CHAPTER): 
            return ("гл." if short_val else "Глава")
        if (typ == InstrumentKind.ITEM): 
            return ("п." if short_val else "Пункт")
        if (typ == InstrumentKind.PARAGRAPH): 
            return ("§" if short_val else "Параграф")
        if (typ == InstrumentKind.SUBPARAGRAPH): 
            return ("подпарагр." if short_val else "Подпараграф")
        if (typ == InstrumentKind.DOCPART): 
            return ("ч." if short_val else "Часть")
        if (typ == InstrumentKind.SECTION): 
            return ("раздел" if short_val else "Раздел")
        if (typ == InstrumentKind.INTERNALDOCUMENT): 
            return "Документ"
        if (typ == InstrumentKind.SUBITEM): 
            return ("пп." if short_val else "Подпункт")
        if (typ == InstrumentKind.SUBSECTION): 
            return ("подразд." if short_val else "Подраздел")
        if (typ == InstrumentKind.CLAUSEPART): 
            return ("ч." if short_val else "Часть")
        if (typ == InstrumentKind.INDENTION): 
            return ("абз." if short_val else "Абзац")
        if (typ == InstrumentKind.PREAMBLE): 
            return ("преамб." if short_val else "Преамбула")
        return None