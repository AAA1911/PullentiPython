﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.ner.named.NamedEntityKind import NamedEntityKind
from pullenti.ner.core.IntOntologyItem import IntOntologyItem


class NamedEntityReferent(Referent):
    """ Текоторые мелкие именованные сущности сущность """
    
    def __init__(self) -> None:
        from pullenti.ner.named.internal.MetaNamedEntity import MetaNamedEntity
        super().__init__(NamedEntityReferent.OBJ_TYPENAME)
        self.instance_of = MetaNamedEntity.GLOBAL_META
    
    OBJ_TYPENAME = "NAMEDENTITY"
    
    ATTR_NAME = "NAME"
    
    ATTR_KIND = "KIND"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_REF = "REF"
    
    ATTR_MISC = "MISC"
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        res = Utils.newStringIO(None)
        typ = self.get_string_value(NamedEntityReferent.ATTR_TYPE)
        if (typ is not None): 
            print(typ, end="", file=res)
        name = self.get_string_value(NamedEntityReferent.ATTR_NAME)
        if (name is not None): 
            if (res.tell() > 0): 
                print(' ', end="", file=res)
            print(MiscHelper.convert_first_char_upper_and_other_lower(name), end="", file=res)
        re = (self.get_value(NamedEntityReferent.ATTR_REF) if isinstance(self.get_value(NamedEntityReferent.ATTR_REF), Referent) else None)
        if (re is not None): 
            if (res.tell() > 0): 
                print("; ", end="", file=res)
            print(re.to_string(short_variant, lang, lev + 1), end="", file=res)
        return Utils.toStringStringIO(res)
    
    @property
    def kind(self) -> 'NamedEntityKind':
        """ Класс сущности """
        str0 = self.get_string_value(NamedEntityReferent.ATTR_KIND)
        if (str0 is None): 
            return NamedEntityKind.UNDEFINED
        try: 
            return Utils.valToEnum(str0, NamedEntityKind)
        except Exception as ex1467: 
            pass
        return NamedEntityKind.UNDEFINED
    
    @kind.setter
    def kind(self, value) -> 'NamedEntityKind':
        self.add_slot(NamedEntityReferent.ATTR_KIND, Utils.enumToString(value).lower(), True, 0)
        return value
    
    def to_sort_string(self) -> str:
        from pullenti.morph.MorphLang import MorphLang
        return Utils.enumToString(self.kind) + self.to_string(True, MorphLang.UNKNOWN, 0)
    
    def get_compare_strings(self) -> typing.List[str]:
        res = list()
        for s in self.slots: 
            if (s.type_name == NamedEntityReferent.ATTR_NAME): 
                str0 = str(s.value)
                if (not str0 in res): 
                    res.append(str0)
                if (str0.find(' ') > 0 or str0.find('-') > 0): 
                    str0 = str0.replace(" ", "").replace("-", "")
                    if (not str0 in res): 
                        res.append(str0)
        if (len(res) == 0): 
            for s in self.slots: 
                if (s.type_name == NamedEntityReferent.ATTR_TYPE): 
                    t = str(s.value)
                    if (not t in res): 
                        res.append(t)
        if (len(res) > 0): 
            return res
        else: 
            return super().get_compare_strings()
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType') -> bool:
        ent = (obj if isinstance(obj, NamedEntityReferent) else None)
        if (ent is None): 
            return False
        if (ent.kind != self.kind): 
            return False
        names = self.get_string_values(NamedEntityReferent.ATTR_NAME)
        names2 = obj.get_string_values(NamedEntityReferent.ATTR_NAME)
        eq_names = False
        if ((names is not None and len(names) > 0 and names2 is not None) and len(names2) > 0): 
            for n in names: 
                if (n in names2): 
                    eq_names = True
            if (not eq_names): 
                return False
        typs = self.get_string_values(NamedEntityReferent.ATTR_TYPE)
        typs2 = obj.get_string_values(NamedEntityReferent.ATTR_TYPE)
        eq_typs = False
        if ((typs is not None and len(typs) > 0 and typs2 is not None) and len(typs2) > 0): 
            for ty in typs: 
                if (ty in typs2): 
                    eq_typs = True
            if (not eq_typs): 
                return False
        if (not eq_typs and not eq_names): 
            return False
        re1 = (self.get_value(NamedEntityReferent.ATTR_REF) if isinstance(self.get_value(NamedEntityReferent.ATTR_REF), Referent) else None)
        re2 = (obj.get_value(NamedEntityReferent.ATTR_REF) if isinstance(obj.get_value(NamedEntityReferent.ATTR_REF), Referent) else None)
        if (re1 is not None and re2 is not None): 
            if (not re1.can_be_equals(re2, typ)): 
                return False
        elif (re1 is not None or re2 is not None): 
            pass
        return True
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        """ Признак того, что была попытка привязаться к внешней онтологии """
        return self._create_ontology_item(2, False, False)
    
    def _create_ontology_item(self, min_len : int, only_names : bool=False, pure_names : bool=False) -> 'IntOntologyItem':
        from pullenti.ner.core.Termin import Termin
        oi = IntOntologyItem(self)
        vars0 = list()
        typs = Utils.ifNotNull(self.get_string_values(NamedEntityReferent.ATTR_TYPE), list())
        for a in self.slots: 
            if (a.type_name == NamedEntityReferent.ATTR_NAME): 
                s = str(a.value).upper()
                if (not s in vars0): 
                    vars0.append(s)
                if (not pure_names): 
                    sp = 0
                    for jj in range(len(s)):
                        if (s[jj] == ' '): 
                            sp += 1
                    if (sp == 1): 
                        s = s.replace(" ", "")
                        if (not s in vars0): 
                            vars0.append(s)
        if (not only_names): 
            if (len(vars0) == 0): 
                for t in typs: 
                    up = t.upper()
                    if (not up in vars0): 
                        vars0.append(up)
        max0 = 20
        cou = 0
        for v in vars0: 
            if (len(v) >= min_len): 
                oi.termins.append(Termin(v))
                cou += 1
                if ((cou) >= max0): 
                    break
        if (len(oi.termins) == 0): 
            return None
        return oi

    
    @staticmethod
    def _new1466(_arg1 : 'NamedEntityKind') -> 'NamedEntityReferent':
        res = NamedEntityReferent()
        res.kind = _arg1
        return res