﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from enum import IntEnum
from pullenti.ntopy.Utils import Utils
from pullenti.ner.MetaToken import MetaToken

from pullenti.ner.phone.PhoneKind import PhoneKind
from pullenti.ner.phone.internal.PhoneHelper import PhoneHelper
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.LanguageHelper import LanguageHelper


class PhoneItemToken(MetaToken):
    """ Примитив, из которых состоит телефонный номер """
    
    class PhoneItemType(IntEnum):
        NUMBER = 0
        CITYCODE = 1
        DELIM = 2
        PREFIX = 3
        ADDNUMBER = 4
        COUNTRYCODE = 5
        ALT = 6
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        self.item_type = PhoneItemToken.PhoneItemType.NUMBER
        self.value = None
        self.kind = PhoneKind.UNDEFINED
        self.is_in_brackets = False
        super().__init__(begin, end, None)
    
    @property
    def can_be_country_prefix(self) -> bool:
        if (self.value is not None and PhoneHelper.get_country_prefix(self.value) == self.value): 
            return True
        else: 
            return False
    
    def __str__(self) -> str:
        return (Utils.enumToString(self.item_type) + ": " + self.value) + ((("" if self.kind == PhoneKind.UNDEFINED else " ({0})".format(Utils.enumToString(self.kind)))))
    
    @staticmethod
    def try_attach(t0 : 'Token') -> 'PhoneItemToken':
        """ Привязать с указанной позиции один примитив
        
        Args:
            cnt: 
            indFrom: 
        
        """
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        res = PhoneItemToken.__try_attach(t0)
        if (res is None): 
            return None
        if (res.item_type != PhoneItemToken.PhoneItemType.PREFIX): 
            return res
        t = res.end_token.next0
        first_pass2876 = True
        while True:
            if first_pass2876: first_pass2876 = False
            else: t = t.next0
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                break
            if (t.is_newline_before): 
                break
            res2 = PhoneItemToken.__try_attach(t)
            if (res2 is not None): 
                if (res2.item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                    if (res.kind == PhoneKind.UNDEFINED): 
                        res.kind = res2.kind
                    res.end_token = res2.end_token
                    t = res.end_token
                    continue
                break
            if (t.is_char(':')): 
                res.end_token = t
                break
            if (not ((isinstance(t, TextToken)))): 
                break
            if (t0.length_char == 1): 
                break
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                t = npt.end_token
                if (t.is_value("ПОСЕЛЕНИЕ", None)): 
                    return None
                res.end_token = t
                continue
            if (t.morph.class0.is_preposition): 
                continue
            break
        return res
    
    @staticmethod
    def __try_attach(t0 : 'Token') -> 'PhoneItemToken':
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.NumberExToken import NumberExToken
        if (t0 is None): 
            return None
        if (isinstance(t0, NumberToken)): 
            if (NumberExToken.try_parse_number_with_postfix(t0) is not None): 
                rt = t0.kit.process_referent("PHONE", t0.next0)
                if (rt is None): 
                    return None
            if ((t0 if isinstance(t0, NumberToken) else None).typ == NumberSpellingType.DIGIT and not t0.morph.class0.is_adjective): 
                return PhoneItemToken._new2282(t0, t0, PhoneItemToken.PhoneItemType.NUMBER, t0.get_source_text())
            return None
        if (t0.is_char('.')): 
            return PhoneItemToken._new2282(t0, t0, PhoneItemToken.PhoneItemType.DELIM, ".")
        if (t0.is_hiphen): 
            return PhoneItemToken._new2282(t0, t0, PhoneItemToken.PhoneItemType.DELIM, "-")
        if (t0.is_char('+')): 
            if (not ((isinstance(t0.next0, NumberToken))) or (t0.next0 if isinstance(t0.next0, NumberToken) else None).typ != NumberSpellingType.DIGIT): 
                return None
            else: 
                val = t0.next0.get_source_text()
                for i in range(len(val)):
                    if (val[i] != '0'): 
                        break
                else: i = len(val)
                if (i >= len(val)): 
                    return None
                if (i > 0): 
                    val = val[i : ]
                return PhoneItemToken._new2282(t0, t0.next0, PhoneItemToken.PhoneItemType.COUNTRYCODE, val)
        if (t0.is_char(chr(0x2011)) and isinstance(t0.next0, NumberToken) and t0.next0.length_char == 2): 
            return PhoneItemToken._new2282(t0, t0, PhoneItemToken.PhoneItemType.DELIM, "-")
        if (t0.is_char_of("(")): 
            if (isinstance(t0.next0, NumberToken)): 
                et = t0.next0
                val = Utils.newStringIO(None)
                while et is not None: 
                    if (et.is_char(')')): 
                        break
                    if (((isinstance(et, NumberToken))) and (et if isinstance(et, NumberToken) else None).typ == NumberSpellingType.DIGIT): 
                        print(et.get_source_text(), end="", file=val)
                    elif (not et.is_hiphen and not et.is_char('.')): 
                        return None
                    et = et.next0
                if (et is None or val.tell() == 0): 
                    return None
                else: 
                    return PhoneItemToken._new2287(t0, et, PhoneItemToken.PhoneItemType.CITYCODE, Utils.toStringStringIO(val), True)
            else: 
                tt1 = PhoneItemToken.__m_phone_termins.try_parse(t0.next0, TerminParseAttr.NO)
                if (tt1 is None or tt1.termin.tag is not None): 
                    pass
                elif (tt1.end_token.next0 is None or not tt1.end_token.next0.is_char(')')): 
                    pass
                else: 
                    return PhoneItemToken._new2288(t0, tt1.end_token.next0, PhoneItemToken.PhoneItemType.PREFIX, True, "")
                return None
        if ((t0.is_char('/') and isinstance(t0.next0, NumberToken) and t0.next0.next0 is not None) and t0.next0.next0.is_char('/') and t0.next0.length_char == 3): 
            return PhoneItemToken._new2287(t0, t0.next0.next0, PhoneItemToken.PhoneItemType.CITYCODE, str((t0.next0 if isinstance(t0.next0, NumberToken) else None).value), True)
        t1 = None
        ki = PhoneKind.UNDEFINED
        if ((t0.is_value("Т", None) and t0.next0 is not None and t0.next0.is_char_of("\\/")) and t0.next0.next0 is not None and ((t0.next0.next0.is_value("Р", None) or t0.next0.next0.is_value("М", None)))): 
            t1 = t0.next0.next0
            ki = (PhoneKind.WORK if t1.is_value("Р", None) else PhoneKind.MOBILE)
        else: 
            tt = PhoneItemToken.__m_phone_termins.try_parse(t0, TerminParseAttr.NO)
            if (tt is None or tt.termin.tag is not None): 
                if (t0.is_value("НОМЕР", None)): 
                    rr = PhoneItemToken.__try_attach(t0.next0)
                    if (rr is not None and rr.item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                        rr.begin_token = t0
                        return rr
                return None
            if (isinstance(tt.termin.tag2, PhoneKind)): 
                ki = Utils.valToEnum(tt.termin.tag2, PhoneKind)
            t1 = tt.end_token
        res = PhoneItemToken._new2290(t0, t1, PhoneItemToken.PhoneItemType.PREFIX, "", ki)
        while True:
            if (t1.next0 is not None and t1.next0.is_char_of(".:")): 
                t1 = t1.next0
                res.end_token = t1
            elif (t1.next0 is not None and t1.next0.is_table_control_char): 
                t1 = t1.next0
            else: 
                break
        if (t0 == t1 and ((t0.begin_char == t0.end_char or t0.chars.is_all_upper))): 
            if (not t0.is_whitespace_after): 
                return None
        return res
    
    @staticmethod
    def try_attach_additional(t0 : 'Token') -> 'PhoneItemToken':
        from pullenti.ner.NumberToken import NumberToken
        t = t0
        if (t is None): 
            return None
        if (t.is_char(',')): 
            t = t.next0
        elif (t.is_char_of("*#") and isinstance(t.next0, NumberToken)): 
            val0 = (t.next0 if isinstance(t.next0, NumberToken) else None).get_source_text()
            t1 = t.next0
            if ((t1.next0 is not None and t1.next0.is_hiphen and not t1.is_whitespace_after) and isinstance(t1.next0.next0, NumberToken) and not t1.next0.is_whitespace_after): 
                t1 = t1.next0.next0
                val0 += t1.get_source_text()
            if (len(val0) >= 3 and (len(val0) < 7)): 
                return PhoneItemToken._new2282(t, t1, PhoneItemToken.PhoneItemType.ADDNUMBER, val0)
        br = False
        if (t is not None and t.is_char('(')): 
            br = True
            t = t.next0
        to = PhoneItemToken.__m_phone_termins.try_parse(t, TerminParseAttr.NO)
        if (to is None): 
            if (not br): 
                return None
            if (t0.whitespaces_before_count > 1): 
                return None
        elif (to.termin.tag is None): 
            return None
        else: 
            t = to.end_token.next0
        if (t is None): 
            return None
        if (((t.is_value("НОМЕР", None) or t.is_value("N", None) or t.is_value("#", None)) or t.is_value("№", None) or t.is_value("NUMBER", None)) or ((t.is_char('+') and br))): 
            t = t.next0
        elif (to is None and not br): 
            return None
        elif (t.is_value("НОМ", None) or t.is_value("ТЕЛ", None)): 
            t = t.next0
            if (t is not None and t.is_char('.')): 
                t = t.next0
        if (t is not None and t.is_char_of(":,") and not t.is_newline_after): 
            t = t.next0
        if (not ((isinstance(t, NumberToken)))): 
            return None
        val = (t if isinstance(t, NumberToken) else None).get_source_text()
        if ((t.next0 is not None and t.next0.is_hiphen and not t.is_whitespace_after) and isinstance(t.next0.next0, NumberToken)): 
            val += t.next0.next0.get_source_text()
            t = t.next0.next0
        if ((len(val) < 2) or len(val) > 7): 
            return None
        if (br): 
            if (t.next0 is None or not t.next0.is_char(')')): 
                return None
            t = t.next0
        res = PhoneItemToken._new2282(t0, t, PhoneItemToken.PhoneItemType.ADDNUMBER, val)
        return res
    
    @staticmethod
    def try_attach_all(t0 : 'Token') -> typing.List['PhoneItemToken']:
        """ Привязать примитивы в контейнере с указанной позиции
        
        Args:
            cnt: 
            indFrom: 
        
        Returns:
            typing.List[PhoneItemToken]: Список примитивов
        """
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        if (t0 is None): 
            return None
        p = PhoneItemToken.try_attach(t0)
        br = False
        if (p is None and t0.is_char('(')): 
            br = True
            p = PhoneItemToken.try_attach(t0.next0)
            if (p is not None): 
                p.begin_token = t0
                p.is_in_brackets = True
                if (p.item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                    br = False
        if (p is None or p.item_type == PhoneItemToken.PhoneItemType.DELIM): 
            return None
        res = list()
        res.append(p)
        t = p.end_token.next0
        first_pass2877 = True
        while True:
            if first_pass2877: first_pass2877 = False
            else: t = t.next0
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                if (len(res) == 1 and res[0].item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                    continue
                else: 
                    break
            if (br and t.is_char(')')): 
                br = False
                continue
            p0 = PhoneItemToken.try_attach(t)
            if (p0 is None): 
                if (t.is_newline_before): 
                    break
                if (p.item_type == PhoneItemToken.PhoneItemType.PREFIX and ((t.is_char_of("\\/") or t.is_hiphen))): 
                    p0 = PhoneItemToken.try_attach(t.next0)
                    if (p0 is not None and p0.item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                        p.end_token = p0.end_token
                        t = p.end_token
                        continue
                if ((res[0].item_type == PhoneItemToken.PhoneItemType.PREFIX and t.is_char_of("\\/") and not t.is_whitespace_after) and not t.is_whitespace_before and isinstance(t.next0, NumberToken)): 
                    sum_num = 0
                    for pp in res: 
                        if (pp.item_type == PhoneItemToken.PhoneItemType.CITYCODE or pp.item_type == PhoneItemToken.PhoneItemType.COUNTRYCODE or pp.item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                            sum_num += len(pp.value)
                    if (sum_num < 7): 
                        tt = t.next0
                        while tt is not None: 
                            if (tt.is_whitespace_before): 
                                break
                            elif (isinstance(tt, NumberToken)): 
                                sum_num += tt.length_char
                            elif (isinstance(tt, TextToken) and not tt.chars.is_letter): 
                                pass
                            else: 
                                break
                            tt = tt.next0
                        if (sum_num == 10 or sum_num == 11): 
                            continue
                if (p0 is None): 
                    break
            if (t.is_newline_before): 
                if (p.item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                    pass
                else: 
                    break
            if (t.whitespaces_before_count > 1): 
                ok = False
                for pp in res: 
                    if (pp.item_type == PhoneItemToken.PhoneItemType.PREFIX or pp.item_type == PhoneItemToken.PhoneItemType.COUNTRYCODE): 
                        ok = True
                        break
                if (not ok): 
                    break
            if (br and p.item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                p.item_type = PhoneItemToken.PhoneItemType.CITYCODE
            p = p0
            if (p.item_type == PhoneItemToken.PhoneItemType.NUMBER and res[len(res) - 1].item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                res.append(PhoneItemToken._new2282(t, t, PhoneItemToken.PhoneItemType.DELIM, " "))
            if (br): 
                p.is_in_brackets = True
            res.append(p)
            t = p.end_token
        p = PhoneItemToken.try_attach_additional(t)
        if ((p) is not None): 
            res.append(p)
        i = 1
        while i < (len(res) - 1): 
            if (res[i].item_type == PhoneItemToken.PhoneItemType.DELIM and res[i + 1].is_in_brackets): 
                del res[i]
                break
            elif (res[i].item_type == PhoneItemToken.PhoneItemType.DELIM and res[i + 1].item_type == PhoneItemToken.PhoneItemType.DELIM): 
                res[i].end_token = res[i + 1].end_token
                del res[i + 1]
                i -= 1
            i += 1
        if ((len(res) > 1 and res[0].is_in_brackets and res[0].item_type == PhoneItemToken.PhoneItemType.PREFIX) and res[len(res) - 1].end_token.next0 is not None and res[len(res) - 1].end_token.next0.is_char(')')): 
            res[len(res) - 1].end_token = res[len(res) - 1].end_token.next0
        if (res[0].item_type == PhoneItemToken.PhoneItemType.PREFIX): 
            i = 2
            while i < (len(res) - 1): 
                if (res[i].item_type == PhoneItemToken.PhoneItemType.PREFIX and res[i + 1].item_type != PhoneItemToken.PhoneItemType.PREFIX): 
                    del res[i:i+len(res) - i]
                    break
                i += 1
        return res
    
    @staticmethod
    def try_attach_alternate(t0 : 'Token', ph0 : 'PhoneReferent', pli : typing.List['PhoneItemToken']) -> 'PhoneItemToken':
        from pullenti.ner.NumberToken import NumberToken
        if (t0 is None): 
            return None
        if (t0.is_char_of("\\/") and isinstance(t0.next0, NumberToken) and (t0.next0.end_char - t0.next0.begin_char) <= 1): 
            pli1 = PhoneItemToken.try_attach_all(t0.next0)
            if (pli1 is not None and len(pli1) > 1): 
                if (pli1[len(pli1) - 1].item_type == PhoneItemToken.PhoneItemType.DELIM): 
                    del pli1[len(pli1) - 1]
                if (len(pli1) <= len(pli)): 
                    num = ""
                    for ii in range(len(pli1)):
                        p1 = pli1[ii]
                        p0 = pli[(len(pli) - len(pli1)) + ii]
                        if (p1.item_type != p0.item_type): 
                            break
                        if (p1.item_type != PhoneItemToken.PhoneItemType.NUMBER and p1.item_type != PhoneItemToken.PhoneItemType.DELIM): 
                            break
                        if (p1.item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                            if (p1.length_char != p0.length_char): 
                                break
                            num += p1.value
                    else: ii = len(pli1)
                    if (ii >= len(pli1)): 
                        return PhoneItemToken._new2282(t0, pli1[len(pli1) - 1].end_token, PhoneItemToken.PhoneItemType.ALT, num)
            return PhoneItemToken._new2282(t0, t0.next0, PhoneItemToken.PhoneItemType.ALT, t0.next0.get_source_text())
        if (t0.is_hiphen and isinstance(t0.next0, NumberToken) and (t0.next0.end_char - t0.next0.begin_char) <= 1): 
            t1 = t0.next0.next0
            ok = False
            if (t1 is None): 
                ok = True
            elif (t1.is_newline_before or t1.is_char_of(",.")): 
                ok = True
            if (ok): 
                return PhoneItemToken._new2282(t0, t0.next0, PhoneItemToken.PhoneItemType.ALT, t0.next0.get_source_text())
        if ((t0.is_char('(') and isinstance(t0.next0, NumberToken) and (t0.next0.end_char - t0.next0.begin_char) == 1) and t0.next0.next0 is not None and t0.next0.next0.is_char(')')): 
            return PhoneItemToken._new2282(t0, t0.next0.next0, PhoneItemToken.PhoneItemType.ALT, t0.next0.get_source_text())
        if ((t0.is_char_of("/-") and isinstance(t0.next0, NumberToken) and ph0._m_template is not None) and LanguageHelper.ends_with(ph0._m_template, str(((t0.next0.end_char - t0.next0.begin_char) + 1)))): 
            return PhoneItemToken._new2282(t0, t0.next0, PhoneItemToken.PhoneItemType.ALT, t0.next0.get_source_text())
        return None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.morph.MorphLang import MorphLang
        if (PhoneItemToken.__m_phone_termins is not None): 
            return
        PhoneItemToken.__m_phone_termins = TerminCollection()
        t = Termin("ТЕЛЕФОН", MorphLang.RU, True)
        t.add_abridge("ТЕЛ.")
        t.add_abridge("TEL.")
        t.add_abridge("Т-Н")
        t.add_abridge("Т.")
        t.add_abridge("T.")
        t.add_abridge("TEL.EXT.")
        t.add_variant("ТЛФ", False)
        t.add_variant("ТЛФН", False)
        t.add_abridge("Т/Ф")
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin._new2299("МОБИЛЬНЫЙ", MorphLang.RU, True, PhoneKind.MOBILE)
        t.add_abridge("МОБ.")
        t.add_abridge("Т.М.")
        t.add_abridge("М.Т.")
        t.add_abridge("М.")
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin._new2299("СОТОВЫЙ", MorphLang.RU, True, PhoneKind.MOBILE)
        t.add_abridge("СОТ.")
        t.add_abridge("CELL.")
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin._new2299("РАБОЧИЙ", MorphLang.RU, True, PhoneKind.WORK)
        t.add_abridge("РАБ.")
        t.add_abridge("Т.Р.")
        t.add_abridge("Р.Т.")
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin("ГОРОДСКОЙ", MorphLang.RU, True)
        t.add_abridge("ГОР.")
        t.add_abridge("Г.Т.")
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin._new2299("ДОМАШНИЙ", MorphLang.RU, True, PhoneKind.HOME)
        t.add_abridge("ДОМ.")
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin("КОНТАКТНЫЙ", MorphLang.RU, True)
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin("МНОГОКАНАЛЬНЫЙ", MorphLang.RU, True)
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin._new2299("ФАКС", MorphLang.RU, True, PhoneKind.FAX)
        t.add_abridge("Ф.")
        t.add_abridge("Т/ФАКС")
        t.add_abridge("ТЕЛ/ФАКС")
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin("ЗВОНИТЬ", MorphLang.RU, True)
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin._new2299("ПРИЕМНАЯ", MorphLang.RU, True, PhoneKind.WORK)
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin("PHONE", MorphLang.EN, True)
        t.add_abridge("PH.")
        t.add_variant("TELEFON", True)
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin._new2299("DIRECT LINE", MorphLang.EN, True, PhoneKind.WORK)
        t.add_variant("DIRECT LINES", True)
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin._new2299("MOBILE", MorphLang.EN, True, PhoneKind.MOBILE)
        t.add_abridge("MOB.")
        t.add_variant("MOBIL", True)
        t.add_abridge("M.")
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin._new2299("FAX", MorphLang.EN, True, PhoneKind.FAX)
        t.add_abridge("F.")
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin._new2299("HOME", MorphLang.EN, True, PhoneKind.HOME)
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin("CALL", MorphLang.EN, True)
        t.add_variant("SEDIU", True)
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin("ДОПОЛНИТЕЛЬНЫЙ", MorphLang.RU, True)
        t.tag = t
        t.add_abridge("ДОП.")
        t.add_abridge("EXT.")
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin("ДОБАВОЧНЫЙ", MorphLang.RU, True)
        t.tag = t
        t.add_abridge("ДОБ.")
        t.add_abridge("Д.")
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin("ВНУТРЕННИЙ", MorphLang.RU, True)
        t.tag = t
        t.add_abridge("ВНУТР.")
        t.add_abridge("ВН.")
        t.add_abridge("ВНТ.")
        t.add_abridge("Т.ВН.")
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin("TONE MODE", MorphLang.EN, True)
        t.tag = t
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin("TONE", MorphLang.EN, True)
        t.tag = t
        PhoneItemToken.__m_phone_termins.add(t)
        t = Termin("ADDITIONAL", MorphLang.EN, True)
        t.add_abridge("ADD.")
        t.tag = t
        t.add_variant("INTERNAL", True)
        t.add_abridge("INT.")
        PhoneItemToken.__m_phone_termins.add(t)
    
    __m_phone_termins = None

    
    @staticmethod
    def _new2282(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PhoneItemType', _arg4 : str) -> 'PhoneItemToken':
        res = PhoneItemToken(_arg1, _arg2)
        res.item_type = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new2287(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PhoneItemType', _arg4 : str, _arg5 : bool) -> 'PhoneItemToken':
        res = PhoneItemToken(_arg1, _arg2)
        res.item_type = _arg3
        res.value = _arg4
        res.is_in_brackets = _arg5
        return res
    
    @staticmethod
    def _new2288(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PhoneItemType', _arg4 : bool, _arg5 : str) -> 'PhoneItemToken':
        res = PhoneItemToken(_arg1, _arg2)
        res.item_type = _arg3
        res.is_in_brackets = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new2290(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PhoneItemType', _arg4 : str, _arg5 : 'PhoneKind') -> 'PhoneItemToken':
        res = PhoneItemToken(_arg1, _arg2)
        res.item_type = _arg3
        res.value = _arg4
        res.kind = _arg5
        return res