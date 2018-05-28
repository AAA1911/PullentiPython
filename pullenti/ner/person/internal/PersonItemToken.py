﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
from enum import IntEnum
from pullenti.ntopy.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphBaseInfo import MorphBaseInfo

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.person.internal.ResourceHelper import ResourceHelper


from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphForm import MorphForm
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.person.internal.ShortNameHelper import ShortNameHelper

from pullenti.ner.person.internal.FioTemplateType import FioTemplateType


class PersonItemToken(MetaToken):
    
    class ItemType(IntEnum):
        VALUE = 0
        INITIAL = 1
        REFERENT = 2
        SUFFIX = 3
    
    class ParseAttr(IntEnum):
        NO = 0
        ALTVAR = 1
        CANBELATIN = 2
        CANINITIALBEDIGIT = 4
        CANBELOWER = 8
        MUSTBEITEMALWAYS = 0x10
        """ Всегда выделять элемент, не нелать никакие проверки """
        IGNOREATTRS = 0x20
        NOMINATIVECASE = 0x40
        """ Известно, что персона в именительном падеже """
        SURNAMEPREFIXNOTMERGE = 0x80
        """ Для фамилий префиксы (фон, ван) оформлять отдельным элементом """
    
    class MorphPersonItemVariant(MorphBaseInfo):
        
        def __init__(self, v : str, bi : 'MorphBaseInfo', lastname_ : bool) -> None:
            self.value = None
            self.short_value = None
            super().__init__(None)
            self.value = v
            if (bi is not None): 
                bi.copy_to(self)
        
        def __str__(self) -> str:
            return "{0}: {1}".format(Utils.ifNotNull(self.value, "?"), super().__str__())
    
        
        @staticmethod
        def _new2238(_arg1 : str, _arg2 : 'MorphBaseInfo', _arg3 : bool, _arg4 : str) -> 'MorphPersonItemVariant':
            res = PersonItemToken.MorphPersonItemVariant(_arg1, _arg2, _arg3)
            res.short_value = _arg4
            return res
    
    class MorphPersonItem:
        
        def __init__(self) -> None:
            
            self.__m_morph = None
            self.vars0 = list()
            self.term = None
            self.is_in_dictionary = False
            self.is_in_ontology = False
            self.is_lastname_has_std_tail = False
            self.is_lastname_has_hiphen = False
            self.is_has_std_postfix = False
        
        @property
        def morph(self) -> 'MorphCollection':
            from pullenti.ner.MorphCollection import MorphCollection
            if (self.__m_morph is not None and self.__m_morph.items_count != len(self.vars0)): 
                self.__m_morph = None
            if (self.__m_morph is None): 
                self.__m_morph = MorphCollection()
                for v in self.vars0: 
                    self.__m_morph.add_item(v)
            return self.__m_morph
        
        @property
        def is_china_surname(self) -> bool:
            from pullenti.ner.person.PersonReferent import PersonReferent
            term_ = self.term
            if (term_ is None and len(self.vars0) > 0): 
                term_ = self.vars0[0].value
            if (term_ is None): 
                return False
            if (Utils.indexOfList(PersonItemToken.MorphPersonItem.__m_lastname_asian, term_, 0) >= 0): 
                return True
            tr = PersonReferent._del_surname_end(term_)
            if (Utils.indexOfList(PersonItemToken.MorphPersonItem.__m_lastname_asian, tr, 0) >= 0): 
                return True
            if (Utils.indexOfList(PersonItemToken.MorphPersonItem.__m_lastname_asian, term_ + "Ь", 0) >= 0): 
                return True
            if (term_[len(term_) - 1] == 'Ь'): 
                if (Utils.indexOfList(PersonItemToken.MorphPersonItem.__m_lastname_asian, term_[0 : (len(term_) - 1)], 0) >= 0): 
                    return True
            return False
        
        def __str__(self) -> str:
            res = Utils.newStringIO(None)
            if (self.term is not None): 
                print(self.term, end="", file=res)
            for v in self.vars0: 
                print("; {0}".format(str(v)), end="", file=res, flush=True)
            if (self.is_in_dictionary): 
                print(" - InDictionary", end="", file=res)
            if (self.is_in_ontology): 
                print(" - InOntology", end="", file=res)
            if (self.is_lastname_has_std_tail): 
                print(" - IsLastnameHasStdTail", end="", file=res)
            if (self.is_has_std_postfix): 
                print(" - IsHasStdPostfix", end="", file=res)
            if (self.is_china_surname): 
                print(" - IsChinaSurname", end="", file=res)
            return Utils.toStringStringIO(res)
        
        def merge_hiphen(self, second : 'MorphPersonItem') -> None:
            
            addvars = list()
            for v in self.vars0: 
                ok = 0
                for vv in second.vars0: 
                    if (((vv.gender & v.gender)) != MorphGender.UNDEFINED): 
                        v.value = "{0}-{1}".format(v.value, vv.value)
                        ok += 1
                        break
                if (ok > 0): 
                    continue
                if (v.gender != MorphGender.UNDEFINED): 
                    for vv in second.vars0: 
                        if (vv.gender == MorphGender.UNDEFINED): 
                            v.value = "{0}-{1}".format(v.value, vv.value)
                            ok += 1
                            break
                    if (ok > 0): 
                        continue
                else: 
                    val0 = v.value
                    for vv in second.vars0: 
                        if (vv.gender != MorphGender.UNDEFINED): 
                            if (ok == 0): 
                                v.value = "{0}-{1}".format(val0, vv.value)
                                vv.copy_to(v)
                            else: 
                                addvars.append(PersonItemToken.MorphPersonItemVariant("{0}-{1}".format(val0, vv.value), vv, False))
                            ok += 1
                    if (ok > 0): 
                        continue
                if (len(second.vars0) == 0): 
                    continue
                v.value = "{0}-{1}".format(v.value, second.vars0[0].value)
            self.vars0.extend(addvars)
        
        def add_prefix(self, val : str) -> None:
            if (self.term is not None): 
                self.term = (val + self.term)
            for v in self.vars0: 
                if (v.value is not None): 
                    v.value = (val + v.value)
        
        def add_postfix(self, val : str, gen : 'MorphGender') -> None:
            if (self.term is not None): 
                self.term = "{0}-{1}".format(self.term, val)
            for v in self.vars0: 
                if (v.value is not None): 
                    v.value = "{0}-{1}".format(v.value, val)
                    if (gen != MorphGender.UNDEFINED): 
                        v.gender = gen
            self.is_has_std_postfix = True
            self.is_in_dictionary = False
        
        def merge_with_by_hiphen(self, pi0 : 'MorphPersonItem') -> None:
            
            self.term = "{0}-{1}".format(Utils.ifNotNull(self.term, ""), Utils.ifNotNull(pi0.term, ""))
            if (pi0.is_in_dictionary): 
                self.is_in_dictionary = True
            if (pi0.is_has_std_postfix): 
                self.is_has_std_postfix = True
            self.is_lastname_has_hiphen = True
            if (len(pi0.vars0) == 0): 
                if (pi0.term is not None): 
                    self.add_postfix(pi0.term, MorphGender.UNDEFINED)
                return
            if (len(self.vars0) == 0): 
                if (self.term is not None): 
                    pi0.add_prefix(self.term + "-")
                self.vars0 = pi0.vars0
                return
            res = list()
            for v in self.vars0: 
                for vv in pi0.vars0: 
                    vvv = PersonItemToken.MorphPersonItemVariant("{0}-{1}".format(v.value, vv.value), v, False)
                    res.append(vvv)
            self.vars0 = res
        
        def correct_lastname_variants(self) -> None:
            self.is_lastname_has_std_tail = False
            for v in self.vars0: 
                if (v.value is not None and (((PersonItemToken.MorphPersonItem.ends_with_std_surname(v.value) or LanguageHelper.ends_with(v.value, "АЯ") or LanguageHelper.ends_with(v.value, "ОЙ")) or LanguageHelper.ends_with(v.value, "ИЙ") or LanguageHelper.ends_with(v.value, "ЫЙ")))): 
                    self.is_lastname_has_std_tail = True
                    break
            if (self.is_lastname_has_std_tail): 
                for i in range(len(self.vars0) - 1, -1, -1):
                    if ((((self.vars0[i].value is not None and not PersonItemToken.MorphPersonItem.ends_with_std_surname(self.vars0[i].value) and not LanguageHelper.ends_with(self.vars0[i].value, "АЯ")) and not LanguageHelper.ends_with(self.vars0[i].value, "ОЙ") and not LanguageHelper.ends_with(self.vars0[i].value, "ИЙ")) and not LanguageHelper.ends_with(self.vars0[i].value, "ЫЙ") and not LanguageHelper.ends_with(self.vars0[i].value, "ИХ")) and not LanguageHelper.ends_with(self.vars0[i].value, "ЫХ")): 
                        del self.vars0[i]
                        continue
                    if (self.vars0[i].gender == MorphGender.UNDEFINED): 
                        del0 = False
                        for j in range(len(self.vars0)):
                            if (j != i and self.vars0[j].value == self.vars0[i].value and self.vars0[j].gender != MorphGender.UNDEFINED): 
                                del0 = True
                                break
                        if (del0): 
                            del self.vars0[i]
                            continue
                        t = PersonItemToken.MorphPersonItem.__find_tail(self.vars0[i].value)
                        if (t is not None): 
                            if (t.gender != MorphGender.UNDEFINED): 
                                self.vars0[i].gender = t.gender
                        elif (LanguageHelper.ends_with_ex(self.vars0[i].value, "А", "Я", None, None)): 
                            self.vars0[i].gender = MorphGender.FEMINIE
                        else: 
                            self.vars0[i].gender = MorphGender.MASCULINE
        
        @staticmethod
        def initialize() -> None:
            
            PersonItemToken.MorphPersonItem.__m_lastname_std_tails = list()
            PersonItemToken.MorphPersonItem.__m_lastname_std_tails.append(PersonItemToken.SurnameTail("ОВ", MorphGender.MASCULINE))
            PersonItemToken.MorphPersonItem.__m_lastname_std_tails.append(PersonItemToken.SurnameTail("ОВА", MorphGender.FEMINIE))
            PersonItemToken.MorphPersonItem.__m_lastname_std_tails.append(PersonItemToken.SurnameTail("ЕВ", MorphGender.MASCULINE))
            PersonItemToken.MorphPersonItem.__m_lastname_std_tails.append(PersonItemToken.SurnameTail("ЕВА", MorphGender.FEMINIE))
            PersonItemToken.MorphPersonItem.__m_lastname_std_tails.append(PersonItemToken.SurnameTail("ЄВ", MorphGender.MASCULINE))
            PersonItemToken.MorphPersonItem.__m_lastname_std_tails.append(PersonItemToken.SurnameTail("ЄВА", MorphGender.FEMINIE))
            PersonItemToken.MorphPersonItem.__m_lastname_std_tails.append(PersonItemToken.SurnameTail("ИН", MorphGender.MASCULINE))
            PersonItemToken.MorphPersonItem.__m_lastname_std_tails.append(PersonItemToken.SurnameTail("ИНА", MorphGender.FEMINIE))
            PersonItemToken.MorphPersonItem.__m_lastname_std_tails.append(PersonItemToken.SurnameTail("ІН", MorphGender.MASCULINE))
            PersonItemToken.MorphPersonItem.__m_lastname_std_tails.append(PersonItemToken.SurnameTail("ІНА", MorphGender.FEMINIE))
            for s in ["ЕР", "РН", "ДЗЕ", "ВИЛИ", "ЯН", "УК", "ЮК", "КО", "МАН", "АНН", "ЙН", "СКУ", "СКИ", "СЬКІ", "ИЛО", "ІЛО", "АЛО", "ИК", "СОН", "РА", "НДА", "НДО", "ЕС", "АС", "АВА", "ЛС", "ЛЮС", "ЛЬС", "ЙЗ", "ЕРГ", "ИНГ", "OR", "ER", "OV", "IN", "ERG"]: 
                PersonItemToken.MorphPersonItem.__m_lastname_std_tails.append(PersonItemToken.SurnameTail(s))
            PersonItemToken.MorphPersonItem.__m_latsname_sex_std_tails = list(["ОВ", "ОВА", "ЕВ", "ЄВ", "ЕВА", "ЄВA", "ИН", "ИНА", "ІН", "ІНА", "ИЙ", "АЯ"])
            PersonItemToken.MorphPersonItem.__m_lastname_asian = list()
            for s in Utils.splitString(ResourceHelper.get_string("chinasurnames.txt"), '\n', False): 
                ss = s.strip().upper().replace("Ё", "Е")
                if (not Utils.isNullOrEmpty(ss)): 
                    PersonItemToken.MorphPersonItem.__m_lastname_asian.append(ss)
            m_china_surs = list(Utils.splitString("Чон Чжао Цянь Сунь Ли Чжоу У Чжэн Ван Фэн Чэнь Чу Вэй Цзян Шэнь Хань Ян Чжу Цинь Ю Сюй Хэ Люй Ши Чжан Кун Цао Янь Хуа Цзинь Тао Ци Се Цзоу Юй Бай Шуй Доу Чжан Юнь Су Пань Гэ Си Фань Пэн Лан Лу Чан Ма Мяо Фан Жэнь Юань Лю Бао Ши Тан Фэй Лянь Цэнь Сюэ Лэй Хэ Ни Тэн Инь Ло Би Хао Ань Чан Лэ Фу Пи Бянь Кан Бу Гу Мэн Пин Хуан Му Сяо Яо Шао Чжань Мао Ди Ми Бэй Мин Ху Хван", ' ', False))
            for s in m_china_surs: 
                ss = s.strip().upper().replace("Ё", "Е")
                if (not Utils.isNullOrEmpty(ss)): 
                    if (not ss in PersonItemToken.MorphPersonItem.__m_lastname_asian): 
                        PersonItemToken.MorphPersonItem.__m_lastname_asian.append(ss)
            PersonItemToken.MorphPersonItem.__m_lastname_asian.sort()
        
        __m_lastname_std_tails = None
        
        __m_latsname_sex_std_tails = None
        
        __m_lastname_asian = None
        
        @staticmethod
        def __find_tail(val : str) -> 'SurnameTail':
            if (val is None): 
                return None
            for i in range(len(PersonItemToken.MorphPersonItem.__m_lastname_std_tails)):
                if (LanguageHelper.ends_with(val, PersonItemToken.MorphPersonItem.__m_lastname_std_tails[i].tail)): 
                    return PersonItemToken.MorphPersonItem.__m_lastname_std_tails[i]
            return None
        
        @staticmethod
        def ends_with_std_surname(val : str) -> bool:
            return PersonItemToken.MorphPersonItem.__find_tail(val) is not None
    
        
        @staticmethod
        def _new2187(_arg1 : bool) -> 'MorphPersonItem':
            res = PersonItemToken.MorphPersonItem()
            res.is_has_std_postfix = _arg1
            return res
        
        @staticmethod
        def _new2195(_arg1 : str) -> 'MorphPersonItem':
            res = PersonItemToken.MorphPersonItem()
            res.term = _arg1
            return res
        
        @staticmethod
        def _new2198(_arg1 : str, _arg2 : bool) -> 'MorphPersonItem':
            res = PersonItemToken.MorphPersonItem()
            res.term = _arg1
            res.is_in_ontology = _arg2
            return res
        
        @staticmethod
        def _new2228(_arg1 : bool) -> 'MorphPersonItem':
            res = PersonItemToken.MorphPersonItem()
            res.is_in_ontology = _arg1
            return res
    
    class SurnameTail:
        
        def __init__(self, t : str, g : 'MorphGender'=MorphGender.UNDEFINED) -> None:
            self.tail = None
            self.gender = MorphGender.UNDEFINED
            self.tail = t
            self.gender = g
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        self.typ = PersonItemToken.ItemType.VALUE
        self.value = None
        self.is_in_dictionary = False
        self.is_hiphen_before = False
        self.is_hiphen_after = False
        self.firstname = None
        self.lastname = None
        self.middlename = None
        self.referent = None
        super().__init__(begin, end, None)
    
    @staticmethod
    def _initialize() -> None:
        PersonItemToken.MorphPersonItem.initialize()
    
    def is_asian_item(self, last : bool) -> bool:
        if (self.value is None or self.typ != PersonItemToken.ItemType.VALUE): 
            return False
        if (self.chars.is_all_lower): 
            return False
        if (self.chars.is_all_upper and self.length_char > 1): 
            return False
        sogl = 0
        gl = 0
        prev_glas = False
        for i in range(len(self.value)):
            ch = self.value[i]
            if (not LanguageHelper.is_cyrillic_char(ch)): 
                return False
            elif (LanguageHelper.is_cyrillic_vowel(ch)): 
                if (not prev_glas): 
                    if (gl > 0): 
                        if (not last): 
                            return False
                        if (i == (len(self.value) - 1) and ((ch == 'А' or ch == 'У' or ch == 'Е'))): 
                            break
                        elif (i == (len(self.value) - 2) and ch == 'О' and self.value[i + 1] == 'М'): 
                            break
                    gl += 1
                prev_glas = True
            else: 
                sogl += 1
                prev_glas = False
        if (gl != 1): 
            if (last and gl == 2): 
                pass
            else: 
                return False
        if (sogl > 4): 
            return False
        if (len(self.value) == 1): 
            if (not self.chars.is_all_upper): 
                return False
        elif (not self.chars.is_capital_upper): 
            return False
        return True
    
    def __str__(self) -> str:
        res = Utils.newStringIO(None)
        print("{0} {1}".format(Utils.enumToString(self.typ), Utils.ifNotNull(self.value, "")), end="", file=res, flush=True)
        if (self.firstname is not None): 
            print(" (First: {0})".format(str(self.firstname)), end="", file=res, flush=True)
        if (self.middlename is not None): 
            print(" (Middle: {0})".format(str(self.middlename)), end="", file=res, flush=True)
        if (self.lastname is not None): 
            print(" (Last: {0})".format(str(self.lastname)), end="", file=res, flush=True)
        if (self.referent is not None): 
            print(" Ref: {0}".format(self.referent), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def __add_postfix_info(self, postfix : str, gen : 'MorphGender') -> None:
        
        if (self.value is not None): 
            self.value = "{0}-{1}".format(self.value, postfix)
        if (self.lastname is not None): 
            self.lastname.add_postfix(postfix, gen)
        if (self.firstname is not None): 
            self.firstname.add_postfix(postfix, gen)
        elif (self.lastname is not None): 
            self.firstname = self.lastname
        else: 
            self.firstname = PersonItemToken.MorphPersonItem._new2187(True)
            self.firstname.vars0.append(PersonItemToken.MorphPersonItemVariant(self.value, MorphBaseInfo._new2188(gen), False))
            if (self.lastname is None): 
                self.lastname = self.firstname
        if (self.middlename is not None): 
            self.middlename.add_postfix(postfix, gen)
        elif (self.firstname is not None and not self.chars.is_latin_letter): 
            self.middlename = self.firstname
        self.is_in_dictionary = False
    
    def merge_with_by_hiphen(self, pi0 : 'PersonItemToken') -> None:
        self.end_token = pi0.end_token
        self.value = "{0}-{1}".format(self.value, pi0.value)
        if (self.lastname is not None): 
            if (pi0.lastname is None or len(pi0.lastname.vars0) == 0): 
                self.lastname.add_postfix(pi0.value, MorphGender.UNDEFINED)
            else: 
                self.lastname.merge_with_by_hiphen(pi0.lastname)
        elif (pi0.lastname is not None): 
            pi0.lastname.add_prefix(self.value + "-")
            self.lastname = pi0.lastname
        if (self.firstname is not None): 
            if (pi0.firstname is None or len(pi0.firstname.vars0) == 0): 
                self.firstname.add_postfix(pi0.value, MorphGender.UNDEFINED)
            else: 
                self.firstname.merge_with_by_hiphen(pi0.firstname)
        elif (pi0.firstname is not None): 
            pi0.firstname.add_prefix(self.value + "-")
            self.firstname = pi0.firstname
        if (self.middlename is not None): 
            if (pi0.middlename is None or len(pi0.middlename.vars0) == 0): 
                self.middlename.add_postfix(pi0.value, MorphGender.UNDEFINED)
            else: 
                self.middlename.merge_with_by_hiphen(pi0.middlename)
        elif (pi0.middlename is not None): 
            pi0.middlename.add_prefix(self.value + "-")
            self.middlename = pi0.middlename
    
    @staticmethod
    def try_attach_latin(t : 'Token') -> 'PersonItemToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        
        from pullenti.ner.mail.internal.MailLine import MailLine
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.ner.person.PersonReferent import PersonReferent
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is None): 
            mt = (t if isinstance(t, MetaToken) else None)
            if (mt is not None and mt.begin_token == mt.end_token): 
                res00 = PersonItemToken.try_attach_latin(mt.begin_token)
                if (res00 is not None): 
                    res00.end_token = t
                    res00.begin_token = res00.end_token
                    return res00
            return None
        if (not tt.chars.is_letter): 
            return None
        if (tt.term == "THE"): 
            return None
        if (tt.term == "JR" or tt.term == "JNR" or tt.term == "JUNIOR"): 
            t1 = tt
            if (tt.next0 is not None and tt.next0.is_char('.')): 
                t1 = tt.next0
            return PersonItemToken._new2189(tt, t1, PersonItemToken.ItemType.SUFFIX, "JUNIOR")
        if ((tt.term == "SR" or tt.term == "SNR" or tt.term == "SENIOR") or tt.term == "FITZ" or tt.term == "FILS"): 
            t1 = tt
            if (tt.next0 is not None and tt.next0.is_char('.')): 
                t1 = tt.next0
            return PersonItemToken._new2189(tt, t1, PersonItemToken.ItemType.SUFFIX, "SENIOR")
        initials = (tt.term == "YU" or tt.term == "YA" or tt.term == "CH") or tt.term == "SH"
        if (not initials and len(tt.term) == 2 and tt.chars.is_capital_upper): 
            if (not LanguageHelper.is_latin_vowel(tt.term[0]) and not LanguageHelper.is_latin_vowel(tt.term[1])): 
                initials = True
        if (initials): 
            rii = PersonItemToken._new2191(tt, tt, PersonItemToken.ItemType.INITIAL, tt.term, tt.chars)
            if (tt.next0 is not None and tt.next0.is_char('.')): 
                rii.end_token = tt.next0
            return rii
        if (tt.chars.is_all_lower): 
            if (not tt.term in PersonItemToken.__m_sur_prefixes_lat): 
                return None
        if (tt.chars.is_cyrillic_letter): 
            return None
        if (tt.length_char == 1): 
            if (tt.next0 is None): 
                return None
            if (tt.next0.is_char('.')): 
                return PersonItemToken._new2191(tt, tt.next0, PersonItemToken.ItemType.INITIAL, tt.term, tt.chars)
            if (not tt.next0.is_whitespace_after and not tt.is_whitespace_after and ((tt.term == "D" or tt.term == "O" or tt.term == "M"))): 
                if (BracketHelper.is_bracket(tt.next0, False) and isinstance(tt.next0.next0, TextToken)): 
                    if (tt.next0.next0.chars.is_latin_letter): 
                        pit0 = PersonItemToken.try_attach_latin(tt.next0.next0)
                        if (pit0 is not None and pit0.typ == PersonItemToken.ItemType.VALUE): 
                            pit0.begin_token = tt
                            val = tt.term
                            if (pit0.value is not None): 
                                if (val == "M" and pit0.value.startswith("C")): 
                                    pit0.value = ("MA" + pit0.value)
                                    val = "MA"
                                else: 
                                    pit0.value = (val + pit0.value)
                            if (pit0.lastname is not None): 
                                pit0.lastname.add_prefix(val)
                                pit0.lastname.is_in_dictionary = True
                            elif (pit0.firstname is not None): 
                                pit0.lastname = pit0.firstname
                                pit0.lastname.add_prefix(val)
                                pit0.lastname.is_in_dictionary = True
                            pit0.middlename = None
                            pit0.firstname = pit0.middlename
                            if (not pit0.chars.is_all_upper and not pit0.chars.is_capital_upper): 
                                pit0.chars.is_capital_upper = True
                            return pit0
            if (not LanguageHelper.is_latin_vowel(tt.term[0]) or tt.whitespaces_after_count != 1): 
                nex = PersonItemToken.try_attach_latin(tt.next0)
                if (nex is not None and nex.typ == PersonItemToken.ItemType.VALUE): 
                    return PersonItemToken._new2191(tt, tt, PersonItemToken.ItemType.INITIAL, tt.term, tt.chars)
                return None
            return PersonItemToken._new2191(tt, tt, PersonItemToken.ItemType.VALUE, tt.term, tt.chars)
        if (not MiscHelper.has_vowel(tt)): 
            return None
        if (tt.term in PersonItemToken.__m_sur_prefixes_lat): 
            te = tt.next0
            if (te is not None and te.is_hiphen): 
                te = te.next0
            res = PersonItemToken.try_attach_latin(te)
            if (res is not None): 
                res.value = "{0}-{1}".format(tt.term, res.value)
                res.begin_token = tt
                res.lastname = PersonItemToken.MorphPersonItem()
                res.lastname.vars0.append(PersonItemToken.MorphPersonItemVariant(res.value, MorphBaseInfo(), True))
                res.lastname.is_lastname_has_hiphen = True
                return res
        if (MailLine.is_keyword(tt)): 
            return None
        res = PersonItemToken(tt, tt)
        res.value = tt.term
        cla = tt.get_morph_class_in_dictionary()
        if (cla.is_proper_name or ((cla.is_proper and ((tt.morph.gender == MorphGender.MASCULINE or tt.morph.gender == MorphGender.FEMINIE))))): 
            res.firstname = PersonItemToken.MorphPersonItem._new2195(res.value)
            for wf in tt.morph.items: 
                if ((wf if isinstance(wf, MorphWordForm) else None).is_in_dictionary): 
                    if (wf.class0.is_proper_name): 
                        res.firstname.vars0.append(PersonItemToken.MorphPersonItemVariant(res.value, wf, False))
            if (len(res.firstname.vars0) == 0): 
                res.firstname.vars0.append(PersonItemToken.MorphPersonItemVariant(res.value, None, False))
            res.firstname.is_in_dictionary = True
        if (cla.is_proper_surname): 
            res.lastname = PersonItemToken.MorphPersonItem._new2195(res.value)
            for wf in tt.morph.items: 
                if ((wf if isinstance(wf, MorphWordForm) else None).is_in_dictionary): 
                    if (wf.class0.is_proper_surname): 
                        res.lastname.vars0.append(PersonItemToken.MorphPersonItemVariant(res.value, wf, False))
            if (len(res.lastname.vars0) == 0): 
                res.lastname.vars0.append(PersonItemToken.MorphPersonItemVariant(res.value, None, False))
            res.lastname.is_in_dictionary = True
        if ((not cla.is_proper_name and not cla.is_proper and not cla.is_proper_surname) and not cla.is_undefined): 
            res.is_in_dictionary = True
        res.morph = tt.morph
        ots = None
        if (t is not None and t.kit.ontology is not None and ots is None): 
            ots = t.kit.ontology.attach_token(PersonReferent.OBJ_TYPENAME, t)
        if (ots is not None): 
            if (ots[0].termin.ignore_terms_order): 
                return PersonItemToken._new2197(ots[0].begin_token, ots[0].end_token, PersonItemToken.ItemType.REFERENT, (ots[0].item.tag if isinstance(ots[0].item.tag, PersonReferent) else None), ots[0].morph)
            res.lastname = PersonItemToken.MorphPersonItem._new2198(ots[0].termin.canonic_text, True)
            for ot in ots: 
                if (ot.termin is not None): 
                    mi = ot.morph
                    if (ot.termin.gender == MorphGender.MASCULINE or ot.termin.gender == MorphGender.FEMINIE): 
                        mi = MorphBaseInfo._new2188(ot.termin.gender)
                    res.lastname.vars0.append(PersonItemToken.MorphPersonItemVariant(ot.termin.canonic_text, mi, True))
        if (res.value.startswith("MC")): 
            res.value = ("MAC" + res.value[2 : ])
        if (res.value.startswith("MAC")): 
            res.middlename = None
            res.firstname = res.middlename
            res.lastname = PersonItemToken.MorphPersonItem._new2187(True)
            res.lastname.vars0.append(PersonItemToken.MorphPersonItemVariant(res.value, MorphBaseInfo(), True))
        return res
    
    @staticmethod
    def try_attach(t : 'Token', loc_ont : 'IntOntologyCollection', attrs : 'ParseAttr'=ParseAttr.NO, prev_list : typing.List['PersonItemToken']=None) -> 'PersonItemToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.person.PersonReferent import PersonReferent
        
        from pullenti.morph.CharsInfo import CharsInfo
        if (t is None): 
            return None
        if (isinstance(t, TextToken)): 
            mc = t.get_morph_class_in_dictionary()
            if (mc.is_preposition or mc.is_conjunction or mc.is_misc): 
                if (t.next0 is not None and isinstance(t.next0, ReferentToken)): 
                    if (((attrs & PersonItemToken.ParseAttr.MUSTBEITEMALWAYS)) != PersonItemToken.ParseAttr.NO and not t.chars.is_all_lower): 
                        pass
                    else: 
                        return None
        if (isinstance(t, NumberToken)): 
            nt = (t if isinstance(t, NumberToken) else None)
            if (nt.begin_token == nt.end_token and nt.typ == NumberSpellingType.WORDS and ((not nt.begin_token.chars.is_all_lower or ((attrs & PersonItemToken.ParseAttr.MUSTBEITEMALWAYS)) != PersonItemToken.ParseAttr.NO))): 
                res00 = PersonItemToken.try_attach(nt.begin_token, loc_ont, attrs, prev_list)
                if (res00 is not None): 
                    res00.end_token = t
                    res00.begin_token = res00.end_token
                    return res00
        if (((isinstance(t, TextToken) and t.length_char == 2 and (t if isinstance(t, TextToken) else None).term == "JI") and t.chars.is_all_upper and not t.is_whitespace_after) and t.next0 is not None and t.next0.is_char('.')): 
            re1 = PersonItemToken._new2189(t, t.next0, PersonItemToken.ItemType.INITIAL, "Л")
            re1.chars.is_cyrillic_letter = True
            re1.chars.is_all_upper = True
            return re1
        if (((((isinstance(t, TextToken) and t.length_char == 1 and (t if isinstance(t, TextToken) else None).term == "J") and t.chars.is_all_upper and not t.is_whitespace_after) and isinstance(t.next0, NumberToken) and (t.next0 if isinstance(t.next0, NumberToken) else None).value == 1) and (t.next0 if isinstance(t.next0, NumberToken) else None).typ == NumberSpellingType.DIGIT and t.next0.next0 is not None) and t.next0.next0.is_char('.')): 
            re1 = PersonItemToken._new2189(t, t.next0.next0, PersonItemToken.ItemType.INITIAL, "Л")
            re1.chars.is_cyrillic_letter = True
            re1.chars.is_all_upper = True
            return re1
        if (((((isinstance(t, TextToken) and t.length_char == 1 and (t if isinstance(t, TextToken) else None).term == "I") and t.chars.is_all_upper and not t.is_whitespace_after) and isinstance(t.next0, NumberToken) and (t.next0 if isinstance(t.next0, NumberToken) else None).value == 1) and (t.next0 if isinstance(t.next0, NumberToken) else None).typ == NumberSpellingType.DIGIT and t.next0.next0 is not None) and t.next0.next0.is_char('.')): 
            if (prev_list is not None and prev_list[0].chars.is_cyrillic_letter): 
                re1 = PersonItemToken._new2189(t, t.next0.next0, PersonItemToken.ItemType.INITIAL, "П")
                re1.chars.is_cyrillic_letter = True
                re1.chars.is_all_upper = True
                return re1
        if (loc_ont is not None and len(loc_ont.items) > 1000): 
            loc_ont = None
        res = PersonItemToken.__try_attach(t, loc_ont, attrs, prev_list)
        if (res is not None): 
            return res
        if (t.chars.is_latin_letter and ((attrs & PersonItemToken.ParseAttr.CANBELATIN)) != PersonItemToken.ParseAttr.NO): 
            ots = None
            if (loc_ont is not None): 
                ots = loc_ont.try_attach(t, PersonReferent.OBJ_TYPENAME, False)
            if (t is not None and t.kit.ontology is not None and ots is None): 
                ots = t.kit.ontology.attach_token(PersonReferent.OBJ_TYPENAME, t)
            if (ots is not None and isinstance(t, TextToken)): 
                if (ots[0].termin.ignore_terms_order): 
                    return PersonItemToken._new2197(ots[0].begin_token, ots[0].end_token, PersonItemToken.ItemType.REFERENT, (ots[0].item.tag if isinstance(ots[0].item.tag, PersonReferent) else None), ots[0].morph)
                res = PersonItemToken._new2205(ots[0].begin_token, ots[0].end_token, (t if isinstance(t, TextToken) else None).term, ots[0].chars)
                res.lastname = PersonItemToken.MorphPersonItem._new2198(ots[0].termin.canonic_text, True)
                for ot in ots: 
                    if (ot.termin is not None): 
                        mi = ot.morph
                        if (ot.termin.gender == MorphGender.MASCULINE or ot.termin.gender == MorphGender.FEMINIE): 
                            mi = MorphBaseInfo._new2188(ot.termin.gender)
                        res.lastname.vars0.append(PersonItemToken.MorphPersonItemVariant(ot.termin.canonic_text, mi, True))
                return res
            res = PersonItemToken.try_attach_latin(t)
            if (res is not None): 
                return res
        if ((isinstance(t, NumberToken) and t.length_char == 1 and ((attrs & PersonItemToken.ParseAttr.CANINITIALBEDIGIT)) != PersonItemToken.ParseAttr.NO) and t.next0 is not None and t.next0.is_char_of(".„")): 
            if ((t if isinstance(t, NumberToken) else None).value == 1): 
                return PersonItemToken._new2191(t, t.next0, PersonItemToken.ItemType.INITIAL, "І", CharsInfo._new2208(True))
            if ((t if isinstance(t, NumberToken) else None).value == 0): 
                return PersonItemToken._new2191(t, t.next0, PersonItemToken.ItemType.INITIAL, "О", CharsInfo._new2208(True))
            if ((t if isinstance(t, NumberToken) else None).value == 3): 
                return PersonItemToken._new2191(t, t.next0, PersonItemToken.ItemType.INITIAL, "З", CharsInfo._new2208(True))
        if (((isinstance(t, NumberToken) and t.length_char == 1 and ((attrs & PersonItemToken.ParseAttr.CANINITIALBEDIGIT)) != PersonItemToken.ParseAttr.NO) and t.next0 is not None and t.next0.chars.is_all_lower) and not t.is_whitespace_after and t.next0.length_char > 2): 
            num = (t if isinstance(t, NumberToken) else None).value
            if (num == 3 and t.next0.chars.is_cyrillic_letter): 
                return PersonItemToken._new2191(t, t.next0, PersonItemToken.ItemType.VALUE, "З" + (t.next0 if isinstance(t.next0, TextToken) else None).term, CharsInfo._new2214(True, True))
            if (num == 0 and t.next0.chars.is_cyrillic_letter): 
                return PersonItemToken._new2191(t, t.next0, PersonItemToken.ItemType.VALUE, "О" + (t.next0 if isinstance(t.next0, TextToken) else None).term, CharsInfo._new2214(True, True))
        if ((((isinstance(t, TextToken) and t.length_char == 1 and t.chars.is_letter) and t.chars.is_all_upper and (t.whitespaces_after_count < 2)) and isinstance(t.next0, TextToken) and t.next0.length_char == 1) and t.next0.chars.is_all_lower): 
            cou = 0
            t1 = None
            lat = 0
            cyr = 0
            ch = (t if isinstance(t, TextToken) else None).get_source_text()[0]
            if (t.chars.is_cyrillic_letter): 
                cyr += 1
                if (ord(LanguageHelper.get_lat_for_cyr(ch)) != 0): 
                    lat += 1
            else: 
                lat += 1
                if (ord(LanguageHelper.get_cyr_for_lat(ch)) != 0): 
                    cyr += 1
            tt = t.next0
            while tt is not None: 
                if (tt.whitespaces_before_count > 1): 
                    break
                if (not ((isinstance(tt, TextToken))) or tt.length_char != 1 or not tt.chars.is_all_lower): 
                    break
                t1 = tt
                cou += 1
                ch = (tt if isinstance(tt, TextToken) else None).get_source_text()[0]
                if (tt.chars.is_cyrillic_letter): 
                    cyr += 1
                    if (ord(LanguageHelper.get_lat_for_cyr(ch)) != 0): 
                        lat += 1
                else: 
                    lat += 1
                    if (ord(LanguageHelper.get_cyr_for_lat(ch)) != 0): 
                        cyr += 1
                tt = tt.next0
            if (cou < 2): 
                return None
            if (cou < 5): 
                if (prev_list is not None and len(prev_list) > 0 and prev_list[len(prev_list) - 1].typ == PersonItemToken.ItemType.INITIAL): 
                    pass
                else: 
                    ne = PersonItemToken.try_attach(t1.next0, loc_ont, attrs, None)
                    if (ne is None or ne.typ != PersonItemToken.ItemType.INITIAL): 
                        return None
            is_cyr = cyr >= lat
            if (cyr == lat and t.chars.is_latin_letter): 
                is_cyr = False
            val = Utils.newStringIO(None)
            tt = t
            while tt is not None and tt.end_char <= t1.end_char: 
                ch = (tt if isinstance(tt, TextToken) else None).get_source_text()[0]
                if (is_cyr and LanguageHelper.is_latin_char(ch)): 
                    chh = LanguageHelper.get_cyr_for_lat(ch)
                    if (ord(chh) != 0): 
                        ch = chh
                elif (not is_cyr and LanguageHelper.is_cyrillic_char(ch)): 
                    chh = LanguageHelper.get_lat_for_cyr(ch)
                    if (ord(chh) != 0): 
                        ch = chh
                print(ch.upper(), end="", file=val)
                tt = tt.next0
            res = PersonItemToken._new2189(t, t1, PersonItemToken.ItemType.VALUE, Utils.toStringStringIO(val))
            res.chars = CharsInfo._new2219(True, is_cyr, not is_cyr, True)
            return res
        if (((attrs & PersonItemToken.ParseAttr.MUSTBEITEMALWAYS)) != PersonItemToken.ParseAttr.NO and isinstance(t, TextToken) and not t.chars.is_all_lower): 
            res = PersonItemToken._new2220(t, t, (t if isinstance(t, TextToken) else None).term)
            return res
        return None
    
    @staticmethod
    def __try_attach(t : 'Token', loc_ont : 'IntOntologyCollection', attrs : 'ParseAttr', prev_list : typing.List['PersonItemToken']=None) -> 'PersonItemToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.morph.CharsInfo import CharsInfo
        from pullenti.ner.core.MiscHelper import MiscHelper
        
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.morph.MorphCase import MorphCase
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is None): 
            if (t.chars.is_letter and t.chars.is_capital_upper and isinstance(t, ReferentToken)): 
                rt = (t if isinstance(t, ReferentToken) else None)
                if (rt.begin_token == rt.end_token and not ((isinstance(rt.referent, PersonReferent)))): 
                    res0 = PersonItemToken.__try_attach(rt.begin_token, loc_ont, attrs, None)
                    if (res0 is None): 
                        res0 = PersonItemToken._new2221(rt, rt, rt.referent.to_string(True, t.kit.base_language, 0).upper(), rt.chars, rt.morph)
                        res0.lastname = PersonItemToken.MorphPersonItem._new2195(res0.value)
                    else: 
                        res0.end_token = rt
                        res0.begin_token = res0.end_token
                    if ((t.next0 is not None and t.next0.is_hiphen and isinstance(t.next0.next0, TextToken)) and t.next0.next0.get_morph_class_in_dictionary().is_proper_secname): 
                        res1 = PersonItemToken.try_attach(t.next0.next0, loc_ont, PersonItemToken.ParseAttr.NO, None)
                        if (res1 is not None and res1.middlename is not None): 
                            res1.middlename.add_prefix(res0.value + "-")
                            res1.firstname = res1.middlename
                            res1.begin_token = t
                            return res1
                    return res0
            return None
        if (not tt.chars.is_letter): 
            return None
        if (tt.chars.is_all_lower and ((attrs & PersonItemToken.ParseAttr.CANBELOWER)) == PersonItemToken.ParseAttr.NO): 
            if (not tt.term in PersonItemToken.M_SUR_PREFIXES): 
                if (((tt.term == "Д" and not tt.is_whitespace_after and BracketHelper.is_bracket(tt.next0, True)) and not tt.next0.is_whitespace_after and isinstance(tt.next0.next0, TextToken)) and tt.next0.next0.chars.is_capital_upper): 
                    pass
                else: 
                    return None
        if (tt.length_char == 1 or tt.term == "ДЖ"): 
            if (tt.next0 is None): 
                return None
            ini = tt.term
            ci = CharsInfo(tt.chars)
            if (not tt.chars.is_cyrillic_letter): 
                cyr = LanguageHelper.get_cyr_for_lat(ini[0])
                if (cyr == chr(0)): 
                    return None
                ini = "{0}".format(cyr)
                ci.is_latin_letter = False
                ci.is_cyrillic_letter = True
            if (tt.next0.is_char('.')): 
                return PersonItemToken._new2191(tt, tt.next0, PersonItemToken.ItemType.INITIAL, ini, ci)
            if ((tt.next0.is_char_of(",;„") and prev_list is not None and len(prev_list) > 0) and prev_list[len(prev_list) - 1].typ == PersonItemToken.ItemType.INITIAL): 
                return PersonItemToken._new2191(tt, tt, PersonItemToken.ItemType.INITIAL, ini, ci)
            if ((tt.next0.whitespaces_after_count < 2) and (tt.whitespaces_after_count < 2) and ((tt.term == "Д" or tt.term == "О" or tt.term == "Н"))): 
                if (BracketHelper.is_bracket(tt.next0, False) and isinstance(tt.next0.next0, TextToken)): 
                    if (tt.next0.next0.chars.is_cyrillic_letter): 
                        pit0 = PersonItemToken.try_attach(tt.next0.next0, loc_ont, Utils.valToEnum(attrs | PersonItemToken.ParseAttr.CANBELOWER, PersonItemToken.ParseAttr), prev_list)
                        if (pit0 is not None): 
                            pit0.begin_token = tt
                            if (pit0.value is not None): 
                                pit0.value = (ini + pit0.value)
                            if (pit0.lastname is not None): 
                                pit0.lastname.add_prefix(ini)
                                pit0.lastname.is_in_dictionary = True
                            elif (pit0.firstname is not None): 
                                pit0.lastname = pit0.firstname
                                pit0.lastname.add_prefix(ini)
                                pit0.lastname.is_in_dictionary = True
                            pit0.middlename = None
                            pit0.firstname = pit0.middlename
                            if (not pit0.chars.is_all_upper and not pit0.chars.is_capital_upper): 
                                pit0.chars.is_capital_upper = True
                            return pit0
            if (not LanguageHelper.is_cyrillic_vowel(tt.term[0]) or tt.whitespaces_after_count != 1): 
                return None
            return PersonItemToken._new2191(tt, tt, PersonItemToken.ItemType.VALUE, tt.term, tt.chars)
        if (not tt.chars.is_cyrillic_letter): 
            return None
        if (not MiscHelper.has_vowel(tt)): 
            return None
        ots = None
        if (loc_ont is not None): 
            ots = loc_ont.try_attach(t, PersonReferent.OBJ_TYPENAME, False)
        if (t is not None and t.kit.ontology is not None and ots is None): 
            ots = t.kit.ontology.attach_token(PersonReferent.OBJ_TYPENAME, t)
        sur_prefix = None
        res = None
        if (ots is not None): 
            if (ots[0].termin.ignore_terms_order): 
                return PersonItemToken._new2197(ots[0].begin_token, ots[0].end_token, PersonItemToken.ItemType.REFERENT, (ots[0].item.tag if isinstance(ots[0].item.tag, PersonReferent) else None), ots[0].morph)
            res = PersonItemToken._new2205(ots[0].begin_token, ots[0].end_token, tt.term, ots[0].chars)
            res.lastname = PersonItemToken.MorphPersonItem._new2228(True)
            res.lastname.term = ots[0].termin.canonic_text
            for ot in ots: 
                if (ot.termin is not None): 
                    mi = ot.morph
                    if (ot.termin.gender == MorphGender.MASCULINE): 
                        if (((t.morph.gender & MorphGender.FEMINIE)) != MorphGender.UNDEFINED): 
                            continue
                        mi = MorphBaseInfo._new2188(ot.termin.gender)
                    elif (ot.termin.gender == MorphGender.FEMINIE): 
                        if (((t.morph.gender & MorphGender.MASCULINE)) != MorphGender.UNDEFINED): 
                            continue
                        mi = MorphBaseInfo._new2188(ot.termin.gender)
                    else: 
                        continue
                    res.lastname.vars0.append(PersonItemToken.MorphPersonItemVariant(ot.termin.canonic_text, mi, True))
            if ("-" in ots[0].termin.canonic_text): 
                return res
        else: 
            res = PersonItemToken._new2221(t, t, tt.term, tt.chars, tt.morph)
            if (tt.term in PersonItemToken.M_SUR_PREFIXES): 
                if (((tt.is_value("БЕН", None) or tt.is_value("ВАН", None))) and ((attrs & PersonItemToken.ParseAttr.ALTVAR)) != PersonItemToken.ParseAttr.NO and ((tt.next0 is None or not tt.next0.is_hiphen))): 
                    pass
                else: 
                    if (tt.next0 is not None): 
                        t1 = tt.next0
                        if (t1.is_hiphen): 
                            tt = (t1.next0 if isinstance(t1.next0, TextToken) else None)
                        elif (((attrs & PersonItemToken.ParseAttr.SURNAMEPREFIXNOTMERGE)) != PersonItemToken.ParseAttr.NO and t1.chars.is_all_lower): 
                            tt = None
                        else: 
                            tt = (t1 if isinstance(t1, TextToken) else None)
                        if ((tt is None or tt.is_newline_before or tt.chars.is_all_lower) or not tt.chars.is_cyrillic_letter or (tt.length_char < 3)): 
                            pass
                        else: 
                            sur_prefix = res.value
                            res.value = "{0}-{1}".format(res.value, tt.term)
                            res.morph = tt.morph
                            res.chars = tt.chars
                            res.end_token = tt
                    if (sur_prefix is None): 
                        if (t.chars.is_capital_upper or t.chars.is_all_upper): 
                            return res
                        return None
        if (tt.is_value("ФАМИЛИЯ", "ПРІЗВИЩЕ") or tt.is_value("ИМЯ", "ІМЯ") or tt.is_value("ОТЧЕСТВО", "БАТЬКОВІ")): 
            return None
        if (tt.morph.class0.is_preposition or tt.morph.class0.is_conjunction): 
            if (tt.get_morph_class_in_dictionary().is_proper_name): 
                pass
            elif (tt.next0 is None or not tt.next0.is_char('.')): 
                if (tt.length_char > 1 and tt.chars.is_capital_upper and not MiscHelper.can_be_start_of_sentence(tt)): 
                    pass
                else: 
                    return None
        if (((attrs & PersonItemToken.ParseAttr.MUSTBEITEMALWAYS)) != PersonItemToken.ParseAttr.NO): 
            pass
        else: 
            if (len(tt.term) > 6 and tt.term.startswith("ЗД")): 
                if (MiscHelper.is_not_more_than_one_error("ЗДРАВСТВУЙТЕ", tt)): 
                    return None
                if (MiscHelper.is_not_more_than_one_error("ЗДРАВСТВУЙ", tt)): 
                    return None
            if (tt.length_char > 6 and tt.term.startswith("ПР")): 
                if (MiscHelper.is_not_more_than_one_error("ПРИВЕТСТВУЮ", tt)): 
                    return None
            if (tt.length_char > 6 and tt.term.startswith("УВ")): 
                if (tt.is_value("УВАЖАЕМЫЙ", None)): 
                    return None
            if (tt.length_char > 6 and tt.term.startswith("ДО")): 
                if (tt.is_value("ДОРОГОЙ", None)): 
                    return None
        if (not tt.chars.is_all_upper and not tt.chars.is_capital_upper): 
            if (((attrs & PersonItemToken.ParseAttr.CANINITIALBEDIGIT)) != PersonItemToken.ParseAttr.NO and not tt.chars.is_all_lower): 
                pass
            elif (((attrs & PersonItemToken.ParseAttr.CANBELOWER)) == PersonItemToken.ParseAttr.NO): 
                return None
        adj = None
        for wff in tt.morph.items: 
            wf = (wff if isinstance(wff, MorphWordForm) else None)
            if (wf is None): 
                continue
            if (wf.class0.is_adjective and wf.contains_attr("к.ф.", MorphClass())): 
                if (wf.is_in_dictionary): 
                    if (LanguageHelper.ends_with(tt.term, "НО") or ((tt.next0 is not None and tt.next0.is_hiphen))): 
                        res.is_in_dictionary = True
                continue
            elif (wf.class0.is_adjective and adj is None and (((wf.is_in_dictionary or wf.normal_case.endswith("ЫЙ") or wf.normal_case.endswith("ИЙ")) or wf.normal_case.endswith("АЯ") or wf.normal_case.endswith("ЯЯ")))): 
                adj = wf
            if (wf.class0.is_verb): 
                if (wf.is_in_dictionary): 
                    res.is_in_dictionary = True
                continue
            if (wf.is_in_dictionary): 
                if ((wf.class0.is_adverb or wf.class0.is_preposition or wf.class0.is_conjunction) or wf.class0.is_pronoun or wf.class0.is_personal_pronoun): 
                    res.is_in_dictionary = True
            if (wf.class0.is_proper_surname or sur_prefix is not None): 
                if (res.lastname is None): 
                    res.lastname = PersonItemToken.MorphPersonItem._new2195(tt.term)
                if (adj is not None): 
                    if (not wf.is_in_dictionary and adj.number == MorphNumber.SINGULAR): 
                        val = adj.normal_case
                        res.lastname.vars0.append(PersonItemToken.MorphPersonItemVariant(val, adj, True))
                        if (val == tt.term): 
                            break
                    adj = None
                if (((attrs & PersonItemToken.ParseAttr.NOMINATIVECASE)) != PersonItemToken.ParseAttr.NO): 
                    if (not wf.case.is_undefined and not wf.case.is_nominative): 
                        continue
                v = PersonItemToken.MorphPersonItemVariant(wf.normal_case, wf, True)
                if (wf.normal_case != tt.term and LanguageHelper.ends_with(tt.term, "ОВ")): 
                    v.value = tt.term
                    v.gender = MorphGender.MASCULINE
                elif ((wf.number == MorphNumber.PLURAL and wf.normal_full is not None and wf.normal_full != wf.normal_case) and len(wf.normal_full) > 1): 
                    v.value = wf.normal_full
                    v.number = MorphNumber.SINGULAR
                    if (len(wf.normal_case) > len(tt.term)): 
                        v.value = tt.term
                res.lastname.vars0.append(v)
                if (wf.is_in_dictionary and v.gender == MorphGender.UNDEFINED and wf.gender == MorphGender.UNDEFINED): 
                    v.gender = MorphGender.MASCULINE
                    vv = PersonItemToken.MorphPersonItemVariant(wf.normal_case, wf, True)
                    vv.value = v.value
                    vv.short_value = v.short_value
                    vv.gender = MorphGender.FEMINIE
                    res.lastname.vars0.append(vv)
                if (wf.is_in_dictionary): 
                    res.lastname.is_in_dictionary = True
                if (tt.term.endswith("ИХ") or tt.term.endswith("ЫХ")): 
                    if (res.lastname.vars0[0].value != tt.term): 
                        res.lastname.vars0.insert(0, PersonItemToken.MorphPersonItemVariant(tt.term, MorphBaseInfo._new2234(MorphCase.ALL_CASES, Utils.valToEnum(MorphGender.MASCULINE | MorphGender.FEMINIE, MorphGender), MorphClass._new2233(True)), True))
            if (sur_prefix is not None): 
                continue
            if (wf.class0.is_proper_name and wf.number != MorphNumber.PLURAL): 
                ok = True
                if (t.morph.language.is_ua): 
                    pass
                elif (wf.normal_case is not None and (len(wf.normal_case) < 5)): 
                    pass
                else: 
                    ok = (not LanguageHelper.ends_with(wf.normal_case, "ОВ") and wf.normal_case != "АЛЛ")
                    if (ok): 
                        if (tt.chars.is_all_upper and (tt.length_char < 4)): 
                            ok = False
                if (ok): 
                    if (res.firstname is None): 
                        res.firstname = PersonItemToken.MorphPersonItem._new2195(tt.term)
                    res.firstname.vars0.append(PersonItemToken.MorphPersonItemVariant(wf.normal_case, wf, False))
                    if (wf.is_in_dictionary): 
                        if (not tt.chars.is_all_upper or tt.length_char > 4): 
                            res.firstname.is_in_dictionary = True
            if (not PersonItemToken.MorphPersonItem.ends_with_std_surname(tt.term)): 
                if (wf.class0.is_proper_secname): 
                    if (res.middlename is None): 
                        res.middlename = PersonItemToken.MorphPersonItem._new2195(tt.term)
                    elif (wf.misc.form == MorphForm.SYNONYM): 
                        continue
                    iii = PersonItemToken.MorphPersonItemVariant(wf.normal_case, wf, False)
                    if (iii.value == tt.term): 
                        res.middlename.vars0.insert(0, iii)
                    else: 
                        res.middlename.vars0.append(iii)
                    if (wf.is_in_dictionary): 
                        res.middlename.is_in_dictionary = True
                if (not wf.class0.is_proper and wf.is_in_dictionary): 
                    res.is_in_dictionary = True
            elif (wf.is_in_dictionary and not wf.class0.is_proper and LanguageHelper.ends_with(tt.term, "КО")): 
                res.is_in_dictionary = True
        if (res.lastname is not None): 
            for v in res.lastname.vars0: 
                if (PersonItemToken.MorphPersonItem.ends_with_std_surname(v.value)): 
                    res.lastname.is_lastname_has_std_tail = True
                    break
            if (not res.lastname.is_in_dictionary): 
                if (((not res.lastname.is_in_dictionary and not res.lastname.is_lastname_has_std_tail)) or PersonItemToken.MorphPersonItem.ends_with_std_surname(tt.term)): 
                    v = PersonItemToken.MorphPersonItemVariant(tt.term, None, True)
                    if (LanguageHelper.ends_with_ex(tt.term, "ВА", "НА", None, None)): 
                        res.lastname.vars0.insert(0, v)
                    else: 
                        res.lastname.vars0.append(v)
                    if (PersonItemToken.MorphPersonItem.ends_with_std_surname(v.value) and not res.lastname.is_in_dictionary): 
                        res.lastname.is_lastname_has_std_tail = True
            res.lastname.correct_lastname_variants()
            if (sur_prefix is not None): 
                res.lastname.is_lastname_has_hiphen = True
                res.lastname.term = "{0}-{1}".format(sur_prefix, res.lastname.term)
                for v in res.lastname.vars0: 
                    v.value = "{0}-{1}".format(sur_prefix, v.value)
            if (tt.morph.class0.is_adjective and not res.lastname.is_in_ontology): 
                std_end = False
                for v in res.lastname.vars0: 
                    if (PersonItemToken.MorphPersonItem.ends_with_std_surname(v.value)): 
                        std_end = True
                        break
                if (not std_end and (tt.whitespaces_after_count < 2)): 
                    npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0)
                    if (npt is not None and npt.end_token != npt.begin_token): 
                        if ((prev_list is not None and len(prev_list) == 1 and prev_list[0].firstname is not None) and prev_list[0].firstname.is_in_dictionary and tt.whitespaces_before_count == 1): 
                            pass
                        else: 
                            res.lastname = None
        elif (tt.length_char > 2): 
            res.lastname = PersonItemToken.MorphPersonItem()
            for wf in tt.morph.items: 
                if (not wf.class0.is_verb): 
                    if (wf.contains_attr("к.ф.", MorphClass())): 
                        continue
                    res.lastname.vars0.append(PersonItemToken.MorphPersonItemVariant((wf if isinstance(wf, MorphWordForm) else None).normal_case, wf, True))
                    if (not res.lastname.is_lastname_has_std_tail): 
                        res.lastname.is_lastname_has_std_tail = PersonItemToken.MorphPersonItem.ends_with_std_surname((wf if isinstance(wf, MorphWordForm) else None).normal_case)
            res.lastname.vars0.append(PersonItemToken.MorphPersonItemVariant(tt.term, None, True))
            if (not res.lastname.is_lastname_has_std_tail): 
                res.lastname.is_lastname_has_std_tail = PersonItemToken.MorphPersonItem.ends_with_std_surname(tt.term)
            if (sur_prefix is not None): 
                res.lastname.add_prefix(sur_prefix + "-")
                res.lastname.is_lastname_has_hiphen = True
        if (res.begin_token == res.end_token): 
            if (res.begin_token.get_morph_class_in_dictionary().is_verb and res.lastname is not None): 
                if (not res.lastname.is_lastname_has_std_tail and not res.lastname.is_in_dictionary): 
                    res.lastname = None
            if (res.lastname is not None and res.begin_token.is_value("ЗАМ", None)): 
                return None
            if (res.firstname is not None and isinstance(res.begin_token, TextToken)): 
                if ((res.begin_token if isinstance(res.begin_token, TextToken) else None).term == "ЛЮБОЙ"): 
                    res.firstname = None
            if (res.begin_token.get_morph_class_in_dictionary().is_adjective and res.lastname is not None): 
                npt = NounPhraseHelper.try_parse(res.begin_token, NounPhraseParseAttr.NO, 0)
                if (npt is not None): 
                    if (npt.begin_token != npt.end_token): 
                        if (not res.lastname.is_in_ontology): 
                            res.lastname = None
        if (res.firstname is not None): 
            for i in range(len(res.firstname.vars0)):
                val = res.firstname.vars0[i].value
                di = ShortNameHelper.get_names_for_shortname(val)
                if (di is None): 
                    continue
                g = res.firstname.vars0[i].gender
                if (g != MorphGender.MASCULINE and g != MorphGender.FEMINIE): 
                    fi = True
                    for kp in di: 
                        if (fi): 
                            res.firstname.vars0[i].short_value = val
                            res.firstname.vars0[i].value = kp.name
                            res.firstname.vars0[i].gender = kp.gender
                            fi = False
                        else: 
                            mi = MorphBaseInfo._new2188(kp.gender)
                            res.firstname.vars0.append(PersonItemToken.MorphPersonItemVariant._new2238(kp.name, mi, False, val))
                else: 
                    cou = 0
                    for kp in di: 
                        if (kp.gender == g): 
                            cou += 1
                            if ((cou) < 2): 
                                res.firstname.vars0[i].value = kp.name
                                res.firstname.vars0[i].short_value = val
                            else: 
                                res.firstname.vars0.insert(i + 1, PersonItemToken.MorphPersonItemVariant._new2238(kp.name, res.firstname.vars0[i], False, val))
        if (res is not None and res.is_in_dictionary and res.firstname is None): 
            wi = res.kit.statistics.get_word_info(res.begin_token)
            if (wi is not None and wi.lower_count > 0): 
                if (((t.morph.class0.is_preposition or t.morph.class0.is_conjunction or t.morph.class0.is_pronoun)) and not MiscHelper.can_be_start_of_sentence(t)): 
                    pass
                else: 
                    return None
        if (res.end_token.next0 is not None and res.end_token.next0.is_hiphen and isinstance(res.end_token.next0.next0, TextToken)): 
            ter = (res.end_token.next0.next0 if isinstance(res.end_token.next0.next0, TextToken) else None).term
            if (ter in PersonItemToken.M_ARAB_POSTFIX or ter in PersonItemToken.M_ARAB_POSTFIX_FEM): 
                res.end_token = res.end_token.next0.next0
                res.__add_postfix_info(ter, (MorphGender.FEMINIE if ter in PersonItemToken.M_ARAB_POSTFIX_FEM else MorphGender.MASCULINE))
                if ((ter == "ОГЛЫ" or ter == "КЫЗЫ" or ter == "ГЫЗЫ") or ter == "УГЛИ" or ter == "КЗЫ"): 
                    if (res.firstname is not None and res.middlename is not None): 
                        res.firstname = None
            elif ((not res.is_whitespace_after and not res.end_token.next0.is_whitespace_after and res.end_token.next0.next0.chars == res.begin_token.chars) and res.begin_token == res.end_token): 
                res1 = PersonItemToken.try_attach(res.end_token.next0.next0, loc_ont, PersonItemToken.ParseAttr.NO, None)
                if (res1 is not None and res1.begin_token == res1.end_token): 
                    if (res1.lastname is not None and res.lastname is not None and ((((res1.lastname.is_has_std_postfix or res1.lastname.is_in_dictionary or res1.lastname.is_in_ontology) or res.lastname.is_has_std_postfix or res.lastname.is_in_dictionary) or res.lastname.is_in_ontology))): 
                        res.lastname.merge_hiphen(res1.lastname)
                        if (res.value is not None and res1.value is not None): 
                            res.value = "{0}-{1}".format(res.value, res1.value)
                        res.firstname = None
                        res.middlename = None
                        res.end_token = res1.end_token
                    elif (res.firstname is not None and ((res.firstname.is_in_dictionary or res.firstname.is_in_ontology))): 
                        if (res1.firstname is not None): 
                            if (res.value is not None and res1.value is not None): 
                                res.value = "{0}-{1}".format(res.value, res1.value)
                            res.firstname.merge_hiphen(res1.firstname)
                            res.lastname = None
                            res.middlename = None
                            res.end_token = res1.end_token
                        elif (res1.middlename is not None): 
                            if (res.value is not None and res1.value is not None): 
                                res.value = "{0}-{1}".format(res.value, res1.value)
                            res.end_token = res1.end_token
                            if (res.middlename is not None): 
                                res.middlename.merge_hiphen(res1.middlename)
                            if (res.firstname is not None): 
                                res.firstname.merge_hiphen(res1.middlename)
                                if (res.middlename is None): 
                                    res.middlename = res.firstname
                            if (res.lastname is not None): 
                                res.lastname.merge_hiphen(res1.middlename)
                                if (res.middlename is None): 
                                    res.middlename = res.firstname
                        elif (res1.lastname is not None and not res1.lastname.is_in_dictionary and not res1.lastname.is_in_ontology): 
                            if (res.value is not None and res1.value is not None): 
                                res.value = "{0}-{1}".format(res.value, res1.value)
                            res.firstname.merge_hiphen(res1.lastname)
                            res.lastname = None
                            res.middlename = None
                            res.end_token = res1.end_token
                    elif ((res.firstname is None and res.middlename is None and res.lastname is not None) and not res.lastname.is_in_ontology and not res.lastname.is_in_dictionary): 
                        if (res.value is not None and res1.value is not None): 
                            res.value = "{0}-{1}".format(res.value, res1.value)
                        res.end_token = res1.end_token
                        if (res1.firstname is not None): 
                            res.lastname.merge_hiphen(res1.firstname)
                            res.firstname = res.lastname
                            res.middlename = None
                            res.lastname = res.middlename
                        elif (res1.middlename is not None): 
                            res.lastname.merge_hiphen(res1.middlename)
                            res.middlename = res.lastname
                            res.firstname = None
                        elif (res1.lastname is not None): 
                            res.lastname.merge_hiphen(res1.lastname)
                        elif (res1.value is not None): 
                            for v in res.lastname.vars0: 
                                v.value = "{0}-{1}".format(v.value, res1.value)
                    elif (((res.firstname is None and res.lastname is None and res.middlename is None) and res1.lastname is not None and res.value is not None) and res1.value is not None): 
                        res.lastname = res1.lastname
                        res.lastname.add_prefix(res.value + "-")
                        res.value = "{0}-{1}".format(res.value, res1.value)
                        res.firstname = None
                        res.middlename = None
                        res.end_token = res1.end_token
                    elif (((res.firstname is None and res.lastname is not None and res.middlename is None) and res1.lastname is None and res.value is not None) and res1.value is not None): 
                        res.lastname.add_postfix("-" + res1.value, MorphGender.UNDEFINED)
                        res.value = "{0}-{1}".format(res.value, res1.value)
                        res.firstname = None
                        res.middlename = None
                        res.end_token = res1.end_token
        while (res.end_token.whitespaces_after_count < 3) and isinstance(res.end_token.next0, TextToken):
            ter = (res.end_token.next0 if isinstance(res.end_token.next0, TextToken) else None).term
            if (((ter != "АЛИ" and ter != "ПАША")) or res.end_token.next0.chars.is_all_lower): 
                if (ter in PersonItemToken.M_ARAB_POSTFIX or ter in PersonItemToken.M_ARAB_POSTFIX_FEM): 
                    if (res.end_token.next0.next0 is not None and res.end_token.next0.next0.is_hiphen): 
                        pass
                    else: 
                        res.end_token = res.end_token.next0
                        res.__add_postfix_info(ter, (MorphGender.FEMINIE if ter in PersonItemToken.M_ARAB_POSTFIX_FEM else MorphGender.MASCULINE))
                        if ((ter == "ОГЛЫ" or ter == "КЫЗЫ" or ter == "ГЫЗЫ") or ter == "УГЛИ" or ter == "КЗЫ"): 
                            if (res.firstname is not None and res.middlename is not None): 
                                res.firstname = None
                        continue
            break
        return res
    
    M_SUR_PREFIXES = None
    
    __m_sur_prefixes_lat = None
    
    M_ARAB_POSTFIX = None
    
    M_ARAB_POSTFIX_FEM = None
    
    @staticmethod
    def try_attach_list(t : 'Token', loc_ont : 'IntOntologyCollection', attrs : 'ParseAttr'=ParseAttr.NO, max_count : int=10) -> typing.List['PersonItemToken']:
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.morph.CharsInfo import CharsInfo
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        
        if (t is None): 
            return None
        if (((not ((isinstance(t, TextToken))) or not t.chars.is_letter)) and ((attrs & PersonItemToken.ParseAttr.CANINITIALBEDIGIT)) == PersonItemToken.ParseAttr.NO): 
            if (isinstance(t, ReferentToken) and isinstance(t.get_referent(), GeoReferent) and (t if isinstance(t, ReferentToken) else None).begin_token == (t if isinstance(t, ReferentToken) else None).end_token): 
                pass
            elif (isinstance(t, NumberToken)): 
                nt = (t if isinstance(t, NumberToken) else None)
                if (nt.begin_token == nt.end_token and nt.typ == NumberSpellingType.WORDS and not nt.begin_token.chars.is_all_lower): 
                    pass
                else: 
                    return None
            else: 
                return None
        pit = PersonItemToken.try_attach(t, loc_ont, attrs, None)
        if (pit is None and t.chars.is_latin_letter): 
            pass
        if (pit is None): 
            return None
        res = list()
        res.append(pit)
        t = pit.end_token.next0
        if ((t is not None and t.is_char('.') and pit.typ == PersonItemToken.ItemType.VALUE) and pit.length_char > 3): 
            str0 = pit.get_source_text()
            if (str0[0].isupper() and str0[len(str0) - 1].isupper()): 
                ok = True
                i = 1
                while i < (len(str0) - 1): 
                    if (not str0[i].islower()): 
                        ok = False
                    i += 1
                if (ok): 
                    pit.value = pit.value[0 : (len(pit.value) - 1)]
                    pit.lastname = None
                    pit.middlename = pit.lastname
                    pit.firstname = pit.middlename
                    pit2 = PersonItemToken._new2189(t, t, PersonItemToken.ItemType.INITIAL, str0[len(str0) - 1 : ])
                    res.append(pit2)
                    t = t.next0
        zap = False
        while t is not None: 
            if (t.whitespaces_before_count > 15): 
                break
            tt = t
            if (tt.is_hiphen and tt.next0 is not None): 
                if (not tt.is_whitespace_after and not tt.is_whitespace_before): 
                    tt = t.next0
                elif (tt.previous.chars == tt.next0.chars and not tt.is_newline_after): 
                    tt = tt.next0
            elif ((tt.is_char(',') and (tt.whitespaces_after_count < 2) and tt.next0 is not None) and len(res) == 1): 
                zap = True
                tt = tt.next0
            elif ((tt.is_char('(') and isinstance(tt.next0, TextToken) and tt.next0.chars == tt.previous.chars) and tt.next0.next0 is not None and tt.next0.next0.is_char(')')): 
                pit0 = res[len(res) - 1]
                pit11 = PersonItemToken.try_attach(tt.next0, loc_ont, attrs, None)
                if (pit0.firstname is not None and pit11 is not None and pit11.firstname is not None): 
                    pit0.firstname.vars0.extend(pit11.firstname.vars0)
                    tt = tt.next0.next0
                    pit0.end_token = tt
                    tt = tt.next0
                elif (pit0.lastname is not None and ((pit0.lastname.is_in_dictionary or pit0.lastname.is_lastname_has_std_tail or pit0.lastname.is_has_std_postfix))): 
                    if (pit11 is not None and pit11.lastname is not None): 
                        if ((pit11.lastname.is_in_dictionary or pit11.lastname.is_lastname_has_std_tail or pit11.lastname.is_has_std_postfix)): 
                            pit0.lastname.vars0.extend(pit11.lastname.vars0)
                            tt = tt.next0.next0
                            pit0.end_token = tt
                            tt = tt.next0
            pit1 = PersonItemToken.try_attach(tt, loc_ont, attrs, res)
            if (pit1 is None): 
                break
            if (pit1.chars.is_cyrillic_letter != pit.chars.is_cyrillic_letter): 
                ok = False
                if (pit1.typ == PersonItemToken.ItemType.INITIAL): 
                    if (pit1.chars.is_cyrillic_letter): 
                        v = LanguageHelper.get_lat_for_cyr(pit1.value[0])
                        if (v != chr(0)): 
                            pit1.value = "{0}".format(v)
                            ok = True
                            pit1.chars = CharsInfo._new2241(True)
                        elif (pit.typ == PersonItemToken.ItemType.INITIAL): 
                            v = LanguageHelper.get_cyr_for_lat(pit.value[0])
                            if (v != chr(0)): 
                                pit.value = "{0}".format(v)
                                ok = True
                                pit.chars = CharsInfo._new2208(True)
                                pit = pit1
                    else: 
                        v = LanguageHelper.get_cyr_for_lat(pit1.value[0])
                        if (v != chr(0)): 
                            pit1.value = "{0}".format(v)
                            ok = True
                            pit1.chars = CharsInfo._new2208(True)
                        elif (pit.typ == PersonItemToken.ItemType.INITIAL): 
                            v = LanguageHelper.get_lat_for_cyr(pit.value[0])
                            if (v != chr(0)): 
                                pit.value = "{0}".format(v)
                                ok = True
                                pit.chars = CharsInfo._new2241(True)
                                pit = pit1
                elif (pit.typ == PersonItemToken.ItemType.INITIAL): 
                    if (pit.chars.is_cyrillic_letter): 
                        v = LanguageHelper.get_lat_for_cyr(pit.value[0])
                        if (v != chr(0)): 
                            pit.value = "{0}".format(v)
                            ok = True
                        elif (pit1.typ == PersonItemToken.ItemType.INITIAL): 
                            v = LanguageHelper.get_cyr_for_lat(pit1.value[0])
                            if (v != chr(0)): 
                                pit1.value = "{0}".format(v)
                                ok = True
                                pit = pit1
                    else: 
                        v = LanguageHelper.get_cyr_for_lat(pit.value[0])
                        if (v != chr(0)): 
                            pit.value = "{0}".format(v)
                            ok = True
                        elif (pit1.typ == PersonItemToken.ItemType.INITIAL): 
                            v = LanguageHelper.get_lat_for_cyr(pit1.value[0])
                            if (v != chr(0)): 
                                pit.value = "{0}".format(v)
                                ok = True
                                pit = pit1
                if (not ok): 
                    break
            if (pit1.typ == PersonItemToken.ItemType.VALUE or ((pit1.typ == PersonItemToken.ItemType.SUFFIX and pit1.is_newline_before))): 
                if (loc_ont is not None and ((attrs & PersonItemToken.ParseAttr.IGNOREATTRS)) == PersonItemToken.ParseAttr.NO): 
                    pat = PersonAttrToken.try_attach(pit1.begin_token, loc_ont, PersonAttrToken.PersonAttrAttachAttrs.NO)
                    if (pat is not None): 
                        if (pit1.is_newline_before): 
                            break
                        if (pit1.lastname is None or not pit1.lastname.is_lastname_has_std_tail): 
                            ty = pit1.begin_token.get_morph_class_in_dictionary()
                            if (ty.is_noun): 
                                if (pit1.whitespaces_before_count > 1): 
                                    break
                                if (pat.chars.is_capital_upper and pat.begin_token == pat.end_token): 
                                    pass
                                else: 
                                    break
            if (tt != t): 
                pit1.is_hiphen_before = True
                res[len(res) - 1].is_hiphen_after = True
            res.append(pit1)
            t = pit1.end_token
            if (len(res) > 10): 
                break
            if (max_count > 0 and len(res) >= max_count): 
                break
            t = (None if t is None else t.next0)
        if (res[0].is_asian_item(False) and len(res[0].value) == 1): 
            if (((attrs & PersonItemToken.ParseAttr.MUSTBEITEMALWAYS)) == PersonItemToken.ParseAttr.NO): 
                if (len(res) < 2): 
                    return None
                if (not res[1].is_asian_item(False) or len(res[1].value) == 1): 
                    return None
        if (zap and len(res) > 1): 
            ok = False
            if (res[0].lastname is not None and len(res) == 3): 
                if (res[1].typ == PersonItemToken.ItemType.INITIAL or res[1].firstname is not None): 
                    if (res[2].typ == PersonItemToken.ItemType.INITIAL or res[2].middlename is not None): 
                        ok = True
            elif (((attrs & PersonItemToken.ParseAttr.CANINITIALBEDIGIT)) != PersonItemToken.ParseAttr.NO and res[0].typ == PersonItemToken.ItemType.VALUE and res[1].typ == PersonItemToken.ItemType.INITIAL): 
                if (len(res) == 2): 
                    ok = True
                elif (len(res) == 3 and res[2].typ == PersonItemToken.ItemType.INITIAL): 
                    ok = True
                elif (len(res) == 3 and res[2].is_in_dictionary): 
                    ok = True
            if (not ok): 
                del res[1:1+len(res) - 1]
        if (len(res) == 1 and res[0].is_newline_before and res[0].is_newline_after): 
            if (res[0].lastname is not None and ((res[0].lastname.is_has_std_postfix or res[0].lastname.is_in_dictionary or res[0].lastname.is_lastname_has_std_tail))): 
                res1 = PersonItemToken.try_attach_list(res[0].end_token.next0, loc_ont, PersonItemToken.ParseAttr.CANBELATIN, max_count)
                if (res1 is not None and len(res1) > 0): 
                    if (len(res1) == 2 and ((res1[0].firstname is not None or res1[1].middlename is not None)) and res1[1].is_newline_after): 
                        res.extend(res1)
                    elif (len(res1) == 1 and res1[0].is_newline_after): 
                        res2 = PersonItemToken.try_attach_list(res1[0].end_token.next0, loc_ont, PersonItemToken.ParseAttr.CANBELATIN, max_count)
                        if (res2 is not None and len(res2) == 1 and res2[0].is_newline_after): 
                            if (res1[0].firstname is not None or res2[0].middlename is not None): 
                                res.append(res1[0])
                                res.append(res2[0])
        i = 0
        first_pass2870 = True
        while True:
            if first_pass2870: first_pass2870 = False
            else: i += 1
            if (not (i < len(res))): break
            if (res[i].firstname is not None and res[i].begin_token.is_value("СВЕТА", None)): 
                if (i > 0 and res[i - 1].lastname is not None): 
                    pass
                elif (((i + 1) < len(res)) and ((res[i + 1].lastname is not None or res[i + 1].middlename is not None))): 
                    pass
                else: 
                    continue
                res[i].firstname.vars0[0].value = "СВЕТЛАНА"
            elif (res[i].typ == PersonItemToken.ItemType.VALUE and ((i + 1) < len(res)) and res[i + 1].typ == PersonItemToken.ItemType.SUFFIX): 
                res[i].__add_postfix_info(res[i + 1].value, MorphGender.UNDEFINED)
                res[i].end_token = res[i + 1].end_token
                if (res[i].lastname is None): 
                    res[i].lastname = PersonItemToken.MorphPersonItem._new2187(True)
                    res[i].lastname.vars0.append(PersonItemToken.MorphPersonItemVariant(res[i].value, MorphBaseInfo(), True))
                    res[i].firstname = None
                del res[i + 1]
        if (len(res) > 1 and res[0].is_in_dictionary and ((attrs & PersonItemToken.ParseAttr.MUSTBEITEMALWAYS)) == PersonItemToken.ParseAttr.NO): 
            mc = res[0].begin_token.get_morph_class_in_dictionary()
            if (mc.is_pronoun or mc.is_personal_pronoun): 
                if (res[0].begin_token.is_value("ТОМ", None)): 
                    pass
                else: 
                    return None
        i = 0
        first_pass2871 = True
        while True:
            if first_pass2871: first_pass2871 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].typ == PersonItemToken.ItemType.VALUE and res[i + 1].typ == PersonItemToken.ItemType.VALUE and res[i].end_token.next0.is_hiphen): 
                ok = False
                if (i > 0 and res[i - 1].typ == PersonItemToken.ItemType.INITIAL and (i + 2) == len(res)): 
                    ok = True
                elif (i == 0 and ((i + 2) < len(res)) and res[i + 2].typ == PersonItemToken.ItemType.INITIAL): 
                    ok = True
                if (not ok): 
                    continue
                res[i].end_token = res[i + 1].end_token
                res[i].value = "{0}-{1}".format(res[i].value, res[i + 1].value)
                res[i].middlename = None
                res[i].lastname = res[i].middlename
                res[i].firstname = res[i].lastname
                res[i].is_in_dictionary = False
                del res[i + 1]
                break
        return res
    
    @staticmethod
    def try_parse_person(t : 'Token', prev_pers_template : 'FioTemplateType'=FioTemplateType.UNDEFINED) -> 'ReferentToken':
        """ Это попытка привязать персону со специфического места
        
        Args:
            t(Token): 
            prev_pers_template(FioTemplateType): шаблон от предыдущей персоны (поможет принять решение в случае ошибки)
        
        """
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.person.PersonAnalyzer import PersonAnalyzer
        from pullenti.ner.NumberToken import NumberToken
        if (t is None): 
            return None
        if (isinstance(t.get_referent(), PersonReferent)): 
            rt = (t if isinstance(t, ReferentToken) else None)
            if (rt.begin_token == rt.end_token): 
                tt1 = t.next0
                if (tt1 is not None and tt1.is_comma): 
                    tt1 = tt1.next0
                if (tt1 is not None and (tt1.whitespaces_before_count < 2)): 
                    pits0 = PersonItemToken.try_attach_list(tt1, None, PersonItemToken.ParseAttr.CANINITIALBEDIGIT, 10)
                    if (pits0 is not None and pits0[0].typ == PersonItemToken.ItemType.INITIAL): 
                        str0 = rt.referent.get_string_value(PersonReferent.ATTR_FIRSTNAME)
                        if (str0 is not None and str0.startswith(pits0[0].value)): 
                            res = ReferentToken._new2246(rt.referent, t, pits0[0].end_token, FioTemplateType.SURNAMEI)
                            if (len(pits0) > 1 and pits0[1].typ == PersonItemToken.ItemType.INITIAL): 
                                str0 = rt.referent.get_string_value(PersonReferent.ATTR_MIDDLENAME)
                                if (str0 is not None and str0.startswith(pits0[1].value)): 
                                    res.end_token = pits0[1].end_token
                                    res.misc_attrs = FioTemplateType.SURNAMEII
                            return res
                    if ((((isinstance(tt1, TextToken) and tt1.length_char == 1 and tt1.chars.is_all_upper) and tt1.chars.is_cyrillic_letter and isinstance(tt1.next0, TextToken)) and (tt1.whitespaces_after_count < 2) and tt1.next0.length_char == 1) and tt1.next0.chars.is_all_upper and tt1.next0.chars.is_cyrillic_letter): 
                        str0 = rt.referent.get_string_value(PersonReferent.ATTR_FIRSTNAME)
                        if (str0 is not None and str0.startswith((tt1 if isinstance(tt1, TextToken) else None).term)): 
                            str2 = rt.referent.get_string_value(PersonReferent.ATTR_MIDDLENAME)
                            if (str2 is None or str2.startswith((tt1.next0 if isinstance(tt1.next0, TextToken) else None).term)): 
                                res = ReferentToken._new2246(rt.referent, t, tt1.next0, FioTemplateType.NAMEISURNAME)
                                if (str2 is None): 
                                    rt.referent.add_slot(PersonReferent.ATTR_MIDDLENAME, (tt1.next0 if isinstance(tt1.next0, TextToken) else None).term, False, 0)
                                if (res.end_token.next0 is not None and res.end_token.next0.is_char('.')): 
                                    res.end_token = res.end_token.next0
                                return res
            return rt
        if (t.get_referent() is not None and t.get_referent().type_name == "ORGANIZATION"): 
            rt = (t if isinstance(t, ReferentToken) else None)
            ppp = PersonItemToken.try_parse_person(rt.begin_token, FioTemplateType.UNDEFINED)
            if (ppp is not None and ppp.end_char == rt.end_char): 
                ppp.end_token = rt
                ppp.begin_token = ppp.end_token
                return ppp
        pits = PersonItemToken.try_attach_list(t, None, Utils.valToEnum(PersonItemToken.ParseAttr.CANINITIALBEDIGIT | PersonItemToken.ParseAttr.CANBELATIN, PersonItemToken.ParseAttr), 10)
        if ((pits is None and isinstance(t, TextToken) and t.chars.is_all_lower) and t.length_char > 3): 
            pi0 = PersonItemToken.try_attach(t, None, Utils.valToEnum(PersonItemToken.ParseAttr.CANINITIALBEDIGIT | PersonItemToken.ParseAttr.CANBELATIN | PersonItemToken.ParseAttr.CANBELOWER, PersonItemToken.ParseAttr), None)
            if (pi0 is not None and pi0.lastname is not None and ((pi0.lastname.is_in_dictionary or pi0.lastname.is_lastname_has_std_tail))): 
                pits = PersonItemToken.try_attach_list(pi0.end_token.next0, None, Utils.valToEnum(PersonItemToken.ParseAttr.CANINITIALBEDIGIT | PersonItemToken.ParseAttr.CANBELATIN, PersonItemToken.ParseAttr), 10)
                if (pits is not None and pits[0].typ == PersonItemToken.ItemType.INITIAL and pits[0].chars.is_latin_letter == pi0.chars.is_latin_letter): 
                    pits.insert(0, pi0)
                else: 
                    pits = None
        if (pits is not None and prev_pers_template != FioTemplateType.UNDEFINED and pits[0].typ == PersonItemToken.ItemType.VALUE): 
            tt1 = None
            if (len(pits) == 1 and prev_pers_template == FioTemplateType.SURNAMEI): 
                tt1 = pits[0].end_token.next0
            if (tt1 is not None and tt1.is_comma): 
                tt1 = tt1.next0
            if ((isinstance(tt1, TextToken) and tt1.chars.is_letter and tt1.chars.is_all_upper) and tt1.length_char == 1 and (tt1.whitespaces_before_count < 2)): 
                ii = PersonItemToken._new2191(tt1, tt1, PersonItemToken.ItemType.INITIAL, (tt1 if isinstance(tt1, TextToken) else None).term, tt1.chars)
                pits.append(ii)
            if (len(pits) == 1 and pits[0].is_newline_after and ((prev_pers_template == FioTemplateType.SURNAMEI or prev_pers_template == FioTemplateType.SURNAMEII))): 
                ppp = PersonItemToken.try_attach_list(pits[0].end_token.next0, None, PersonItemToken.ParseAttr.CANBELATIN, 10)
                if (ppp is not None and ppp[0].typ == PersonItemToken.ItemType.INITIAL): 
                    pits.append(ppp[0])
                    if (len(ppp) > 1 and ppp[1].typ == PersonItemToken.ItemType.INITIAL): 
                        pits.append(ppp[1])
        if (pits is not None and len(pits) > 1): 
            tmpls = FioTemplateType.UNDEFINED
            first = None
            middl = None
            last = None
            if (pits[0].typ == PersonItemToken.ItemType.VALUE and pits[1].typ == PersonItemToken.ItemType.INITIAL): 
                first = pits[1]
                last = pits[0]
                tmpls = FioTemplateType.SURNAMEI
                if (len(pits) > 2 and pits[2].typ == PersonItemToken.ItemType.INITIAL): 
                    middl = pits[2]
                    tmpls = FioTemplateType.SURNAMEII
            elif (pits[0].typ == PersonItemToken.ItemType.INITIAL and pits[1].typ == PersonItemToken.ItemType.VALUE): 
                first = pits[0]
                last = pits[1]
                tmpls = FioTemplateType.ISURNAME
            elif ((len(pits) > 2 and pits[0].typ == PersonItemToken.ItemType.INITIAL and pits[1].typ == PersonItemToken.ItemType.INITIAL) and pits[2].typ == PersonItemToken.ItemType.VALUE): 
                first = pits[0]
                middl = pits[1]
                last = pits[2]
                tmpls = FioTemplateType.IISURNAME
            if (len(pits) == 2 and pits[0].typ == PersonItemToken.ItemType.VALUE and pits[1].typ == PersonItemToken.ItemType.VALUE): 
                if (pits[0].chars.is_latin_letter and ((not pits[0].is_in_dictionary or not pits[1].is_in_dictionary))): 
                    if (not MiscHelper.is_eng_article(pits[0].begin_token)): 
                        first = pits[0]
                        last = pits[1]
                        tmpls = FioTemplateType.NAMESURNAME
            if (last is not None): 
                pers = PersonReferent()
                pers.add_slot(PersonReferent.ATTR_LASTNAME, last.value, False, 0)
                pers.add_slot(PersonReferent.ATTR_FIRSTNAME, first.value, False, 0)
                if (middl is not None): 
                    pers.add_slot(PersonReferent.ATTR_MIDDLENAME, middl.value, False, 0)
                res = ReferentToken(pers, t, last.end_token)
                if (first.end_char > last.end_char): 
                    res.end_token = first.end_token
                if (middl is not None and middl.end_char > res.end_char): 
                    res.end_token = middl.end_token
                res.data = t.kit.get_analyzer_data_by_analyzer_name(PersonAnalyzer.ANALYZER_NAME)
                res.misc_attrs = tmpls
                if ((res.end_token.whitespaces_after_count < 2) and isinstance(res.end_token.next0, NumberToken)): 
                    num = (res.end_token.next0 if isinstance(res.end_token.next0, NumberToken) else None)
                    if (num.value == 2 or num.value == 3): 
                        if (num.morph.class0.is_adjective): 
                            pers.add_slot(PersonReferent.ATTR_NICKNAME, str(num.value), False, 0)
                            res.end_token = res.end_token.next0
                return res
        if (pits is not None and len(pits) == 1 and pits[0].typ == PersonItemToken.ItemType.VALUE): 
            tt = pits[0].end_token.next0
            comma = False
            if (tt is not None and ((tt.is_comma or tt.is_char('.')))): 
                tt = tt.next0
                comma = True
            if ((isinstance(tt, TextToken) and tt.length_char == 2 and tt.chars.is_all_upper) and tt.chars.is_cyrillic_letter): 
                pers = PersonReferent()
                pers.add_slot(PersonReferent.ATTR_LASTNAME, pits[0].value, False, 0)
                pers.add_slot(PersonReferent.ATTR_FIRSTNAME, (tt if isinstance(tt, TextToken) else None).term[0], False, 0)
                pers.add_slot(PersonReferent.ATTR_MIDDLENAME, (tt if isinstance(tt, TextToken) else None).term[1], False, 0)
                res = ReferentToken._new2246(pers, t, tt, FioTemplateType.SURNAMEII)
                if (tt.next0 is not None and tt.next0.is_char('.')): 
                    tt = tt.next0
                    res.end_token = tt
                res.data = t.kit.get_analyzer_data_by_analyzer_name(PersonAnalyzer.ANALYZER_NAME)
                return res
            if (((((isinstance(tt, TextToken) and (tt.whitespaces_before_count < 2) and tt.length_char == 1) and tt.chars.is_all_upper and tt.chars.is_cyrillic_letter) and isinstance(tt.next0, TextToken) and (tt.whitespaces_after_count < 2)) and tt.next0.length_char == 1 and tt.next0.chars.is_all_upper) and tt.next0.chars.is_cyrillic_letter): 
                pers = PersonReferent()
                pers.add_slot(PersonReferent.ATTR_LASTNAME, pits[0].value, False, 0)
                pers.add_slot(PersonReferent.ATTR_FIRSTNAME, (tt if isinstance(tt, TextToken) else None).term, False, 0)
                pers.add_slot(PersonReferent.ATTR_MIDDLENAME, (tt.next0 if isinstance(tt.next0, TextToken) else None).term, False, 0)
                res = ReferentToken._new2246(pers, t, tt.next0, FioTemplateType.SURNAMEII)
                if (tt.next0.next0 is not None and tt.next0.next0.is_char('.')): 
                    res.end_token = tt.next0.next0
                res.data = t.kit.get_analyzer_data_by_analyzer_name(PersonAnalyzer.ANALYZER_NAME)
                return res
            if (comma and tt is not None and (tt.whitespaces_before_count < 2)): 
                pits1 = PersonItemToken.try_attach_list(tt, None, Utils.valToEnum(PersonItemToken.ParseAttr.CANINITIALBEDIGIT | PersonItemToken.ParseAttr.CANBELATIN, PersonItemToken.ParseAttr), 10)
                if (pits1 is not None and len(pits1) > 0 and pits1[0].typ == PersonItemToken.ItemType.INITIAL): 
                    if (prev_pers_template != FioTemplateType.UNDEFINED): 
                        if (prev_pers_template != FioTemplateType.SURNAMEI and prev_pers_template != FioTemplateType.SURNAMEII): 
                            return None
                    pers = PersonReferent()
                    pers.add_slot(PersonReferent.ATTR_LASTNAME, pits[0].value, False, 0)
                    nam = pits1[0].value
                    if (pits1[0].chars.is_cyrillic_letter != pits[0].chars.is_cyrillic_letter): 
                        if (pits[0].chars.is_cyrillic_letter): 
                            ch = LanguageHelper.get_cyr_for_lat(nam[0])
                        else: 
                            ch = LanguageHelper.get_lat_for_cyr(nam[0])
                        if (ch != chr(0)): 
                            nam = "{0}".format(ch)
                    pers.add_slot(PersonReferent.ATTR_FIRSTNAME, nam, False, 0)
                    res = ReferentToken._new2246(pers, t, pits1[0].end_token, FioTemplateType.SURNAMEI)
                    if (len(pits1) > 1 and pits1[1].typ == PersonItemToken.ItemType.INITIAL): 
                        mid = pits1[1].value
                        if (pits1[1].chars.is_cyrillic_letter != pits[0].chars.is_cyrillic_letter): 
                            if (pits[0].chars.is_cyrillic_letter): 
                                ch = LanguageHelper.get_cyr_for_lat(mid[0])
                            else: 
                                ch = LanguageHelper.get_lat_for_cyr(mid[0])
                            if (ch != chr(0)): 
                                mid = "{0}".format(ch)
                        pers.add_slot(PersonReferent.ATTR_MIDDLENAME, mid, False, 0)
                        res.end_token = pits1[1].end_token
                        res.misc_attrs = FioTemplateType.SURNAMEII
                    res.data = t.kit.get_analyzer_data_by_analyzer_name(PersonAnalyzer.ANALYZER_NAME)
                    return res
        return None

    
    @staticmethod
    def _new2189(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str) -> 'PersonItemToken':
        res = PersonItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new2191(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : 'CharsInfo') -> 'PersonItemToken':
        res = PersonItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.chars = _arg5
        return res
    
    @staticmethod
    def _new2197(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'PersonReferent', _arg5 : 'MorphCollection') -> 'PersonItemToken':
        res = PersonItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.referent = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new2205(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'CharsInfo') -> 'PersonItemToken':
        res = PersonItemToken(_arg1, _arg2)
        res.value = _arg3
        res.chars = _arg4
        return res
    
    @staticmethod
    def _new2220(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'PersonItemToken':
        res = PersonItemToken(_arg1, _arg2)
        res.value = _arg3
        return res
    
    @staticmethod
    def _new2221(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'CharsInfo', _arg5 : 'MorphCollection') -> 'PersonItemToken':
        res = PersonItemToken(_arg1, _arg2)
        res.value = _arg3
        res.chars = _arg4
        res.morph = _arg5
        return res
    
    # static constructor for class PersonItemToken
    @staticmethod
    def _static_ctor():
        PersonItemToken.M_SUR_PREFIXES = list(["АБД", "АБУ", "АЛ", "АЛЬ", "БИН", "БЕН", "ИБН", "ФОН", "ВАН", "ДЕ", "ДИ", "ДА", "ЛА", "ЛЕ", "ЛЯ", "ЭЛЬ"])
        PersonItemToken.__m_sur_prefixes_lat = list(["ABD", "AL", "BEN", "IBN", "VON", "VAN", "DE", "DI", "LA", "LE", "DA", "DE"])
        PersonItemToken.M_ARAB_POSTFIX = list(["АГА", "АЛИ", "АР", "АС", "АШ", "БЕЙ", "БЕК", "ЗАДЕ", "ОГЛЫ", "УГЛИ", "ОЛЬ", "ООЛ", "ПАША", "УЛЬ", "УЛЫ", "ХАН", "ХАДЖИ", "ШАХ", "ЭД", "ЭЛЬ"])
        PersonItemToken.M_ARAB_POSTFIX_FEM = list(["АСУ", "АЗУ", "ГЫЗЫ", "ЗУЛЬ", "КЫЗЫ", "КЫС", "КЗЫ"])

PersonItemToken._static_ctor()