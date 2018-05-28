﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
from enum import IntEnum
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.MetaToken import MetaToken

from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NumberHelper import NumberHelper

from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.instrument.InstrumentKind import InstrumentKind
from pullenti.ner.instrument.internal.NumberingHelper import NumberingHelper
from pullenti.morph.LanguageHelper import LanguageHelper


class PartToken(MetaToken):
    """ Примитив, из которых состоит часть декрета (статья, пункт и часть) """
    
    class ItemType(IntEnum):
        UNDEFINED = 0
        PREFIX = 1
        APPENDIX = 2
        DOCPART = 3
        PART = 4
        SECTION = 5
        SUBSECTION = 6
        CHAPTER = 7
        CLAUSE = 8
        PARAGRAPH = 9
        SUBPARAGRAPH = 10
        ITEM = 11
        SUBITEM = 12
        INDENTION = 13
        SUBINDENTION = 14
        PREAMBLE = 15
        NOTICE = 16
        SUBPROGRAM = 17
        PAGE = 18
        ADDAGREE = 19
    
    class PartValue(MetaToken):
        
        def __init__(self, begin : 'Token', end : 'Token') -> None:
            self.value = None
            super().__init__(begin, end, None)
        
        @property
        def source_value(self) -> str:
            t0 = self.begin_token
            t1 = self.end_token
            if (t1.is_char('.')): 
                t1 = t1.previous
            elif (t1.is_char(')') and not t0.is_char('(')): 
                t1 = t1.previous
            return (MetaToken(t0, t1)).get_source_text()
        
        @property
        def int_value(self) -> int:
            if (Utils.isNullOrEmpty(self.value)): 
                return 0
            inoutarg961 = RefOutArgWrapper(None)
            inoutres962 = Utils.tryParseInt(self.value, inoutarg961)
            num = inoutarg961.value
            if (inoutres962): 
                return num
            return 0
        
        def __str__(self) -> str:
            return self.value
        
        def correct_value(self) -> None:
            from pullenti.ner.TextToken import TextToken
            from pullenti.ner.core.BracketHelper import BracketHelper
            from pullenti.ner.NumberToken import NumberToken
            from pullenti.ner.decree.DecreeReferent import DecreeReferent
            if ((isinstance(self.end_token.next0, TextToken) and (self.end_token.next0 if isinstance(self.end_token.next0, TextToken) else None).length_char == 1 and self.end_token.next0.chars.is_letter) and not self.end_token.is_whitespace_after): 
                self.value += (self.end_token.next0 if isinstance(self.end_token.next0, TextToken) else None).term
                self.end_token = self.end_token.next0
            if ((BracketHelper.can_be_start_of_sequence(self.end_token.next0, False, False) and isinstance(self.end_token.next0.next0, TextToken) and self.end_token.next0.next0.length_char == 1) and BracketHelper.can_be_end_of_sequence(self.end_token.next0.next0.next0, False, self.end_token.next0, False)): 
                self.value = "{0}.{1}".format(self.value, (self.end_token.next0.next0 if isinstance(self.end_token.next0.next0, TextToken) else None).term)
                self.end_token = self.end_token.next0.next0.next0
            t = self.end_token.next0
            first_pass2644 = True
            while True:
                if first_pass2644: first_pass2644 = False
                else: t = t.next0
                if (not (t is not None)): break
                if (t.is_whitespace_before): 
                    break
                if (t.is_char_of("_.") and not t.is_whitespace_after): 
                    if (isinstance(t.next0, NumberToken)): 
                        self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), (t.next0 if isinstance(t.next0, NumberToken) else None).value)
                        t = t.next0
                        self.end_token = t
                        continue
                    if (((t.next0 is not None and t.next0.is_char('(') and isinstance(t.next0.next0, NumberToken)) and not t.next0.is_whitespace_after and t.next0.next0.next0 is not None) and t.next0.next0.next0.is_char(')')): 
                        self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), (t.next0.next0 if isinstance(t.next0.next0, NumberToken) else None).value)
                        self.end_token = t.next0.next0.next0
                        continue
                if (t.is_hiphen and not t.is_whitespace_after and isinstance(t.next0, NumberToken)): 
                    inoutarg963 = RefOutArgWrapper(None)
                    inoutres964 = Utils.tryParseInt(self.value, inoutarg963)
                    n1 = inoutarg963.value
                    if (inoutres964 and n1 >= (t.next0 if isinstance(t.next0, NumberToken) else None).value): 
                        self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), (t.next0 if isinstance(t.next0, NumberToken) else None).value)
                        t = t.next0
                        self.end_token = t
                        continue
                if ((t.is_char_of("(<") and isinstance(t.next0, NumberToken) and t.next0.next0 is not None) and t.next0.next0.is_char_of(")>")): 
                    self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), (t.next0 if isinstance(t.next0, NumberToken) else None).value)
                    t = t.next0.next0
                    self.end_token = t
                    if (t.next0 is not None and t.next0.is_char('.') and not t.is_whitespace_after): 
                        t = t.next0
                    continue
                break
            if (self.end_token.next0 is not None and self.end_token.next0.is_char_of(".") and not self.end_token.is_whitespace_after): 
                if (self.end_token.next0.next0 is not None and isinstance(self.end_token.next0.next0.get_referent(), DecreeReferent) and not self.end_token.next0.is_newline_after): 
                    self.end_token = self.end_token.next0
            if (self.begin_token == self.end_token and self.end_token.next0 is not None and self.end_token.next0.is_char(')')): 
                ok = True
                lev = 0
                ttt = self.begin_token.previous
                while ttt is not None: 
                    if (ttt.is_newline_after): 
                        break
                    if (ttt.is_char(')')): 
                        lev += 1
                    elif (ttt.is_char('(')): 
                        lev -= 1
                        if (lev < 0): 
                            ok = False
                            break
                    ttt = ttt.previous
                if (ok): 
                    tt = self.end_token.next0.next0
                    if (tt is not None): 
                        if (isinstance(tt.get_referent(), DecreeReferent) or PartToken.try_attach(tt, None, False, False) is not None): 
                            self.end_token = self.end_token.next0
    
        
        @staticmethod
        def _new965(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'PartValue':
            res = PartToken.PartValue(_arg1, _arg2)
            res.value = _arg3
            return res
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        
        self.typ = PartToken.ItemType.UNDEFINED
        self.alt_typ = PartToken.ItemType.UNDEFINED
        self.values = list()
        self.name = None
        self.ind = 0
        self.decree = None
        self.is_doubt = False
        self.delim_after = False
        self.has_terminator = False
        self.anafor_ref = None
        super().__init__(begin, end, None)
    
    def __str__(self) -> str:
        res = Utils.newStringIO(Utils.enumToString(self.typ))
        for v in self.values: 
            print(" {0}".format(v), end="", file=res, flush=True)
        if (self.delim_after): 
            print(", DelimAfter", end="", file=res)
        if (self.is_doubt): 
            print(", Doubt", end="", file=res)
        if (self.has_terminator): 
            print(", Terminator", end="", file=res)
        if (self.anafor_ref is not None): 
            print(", Ref='{0}'".format(self.anafor_ref.term), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def try_attach(t : 'Token', prev : 'PartToken', in_bracket : bool=False, ignore_number : bool=False) -> 'PartToken':
        """ Привязать с указанной позиции один примитив
        
        """
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        if (t is None): 
            return None
        res = None
        if (t.morph.class0.is_personal_pronoun and (t.whitespaces_after_count < 2)): 
            res = PartToken.try_attach(t.next0, prev, False, False)
            if (res is not None): 
                res.anafor_ref = (t if isinstance(t, TextToken) else None)
                res.begin_token = t
                return res
        tt = (t if isinstance(t, TextToken) else None)
        if (isinstance(t, NumberToken) and t.next0 is not None and (t.whitespaces_after_count < 3)): 
            re = PartToken.__create_part_typ0(t.next0, prev)
            if (re is not None): 
                t11 = re.end_token.next0
                ok1 = False
                if (t11 is not None and isinstance(t11.get_referent(), DecreeReferent)): 
                    ok1 = True
                elif (prev is not None and t11 is not None and not ((isinstance(t11, NumberToken)))): 
                    ok1 = True
                if (not ok1): 
                    res1 = PartToken.try_attach(t11, None, False, False)
                    if (res1 is not None): 
                        ok1 = True
                if (ok1 or in_bracket): 
                    re.begin_token = t
                    re.values.append(PartToken.PartValue._new965(t, t, str((t if isinstance(t, NumberToken) else None).value)))
                    return re
        if ((isinstance(t, NumberToken) and (t if isinstance(t, NumberToken) else None).typ == NumberSpellingType.DIGIT and prev is None) and t.previous is not None): 
            t0 = t.previous
            delim = False
            if (t0.is_char(',') or t0.morph.class0.is_conjunction): 
                delim = True
                t0 = t0.previous
            if (t0 is None): 
                return None
            dr = (t0.get_referent() if isinstance(t0.get_referent(), DecreePartReferent) else None)
            if (dr is None): 
                if (t0.is_char('(') and t.next0 is not None): 
                    if (t.next0.is_value("ЧАСТЬ", None) or t.next0.is_value("Ч", None)): 
                        te = t.next0
                        if (te.next0 is not None and te.next0.is_char('.')): 
                            te = te.next0
                        res = PartToken._new746(t, te, PartToken.ItemType.PART)
                        res.values.append(PartToken.PartValue._new965(t, t, str((t if isinstance(t, NumberToken) else None).value)))
                        return res
                return None
            if (dr.clause is None): 
                return None
            res = PartToken._new968(t, t, PartToken.ItemType.CLAUSE, not delim)
            pv = PartToken.PartValue._new965(t, t, str((t if isinstance(t, NumberToken) else None).value))
            res.values.append(pv)
            t = t.next0
            while t is not None: 
                if (t.is_whitespace_before): 
                    break
                elif (t.is_char_of("._") and isinstance(t.next0, NumberToken)): 
                    t = t.next0
                    res.end_token = t
                    pv.end_token = res.end_token
                    pv.value = "{0}.{1}".format(pv.value, (t if isinstance(t, NumberToken) else None).value)
                else: 
                    break
                t = t.next0
            return res
        if (tt is None): 
            return None
        if (tt.length_char == 1 and not tt.chars.is_all_lower): 
            return None
        t1 = tt
        res = PartToken.__create_part_typ0(t1, prev)
        if (res is not None): 
            t1 = res.end_token
        elif ((t1.is_value("СИЛУ", None) or t1.is_value("СОГЛАСНО", None) or t1.is_value("СООТВЕТСТВИЕ", None)) or t1.is_value("ПОЛОЖЕНИЕ", None)): 
            if (t1.is_value("СИЛУ", None) and t1.previous is not None and t1.previous.morph.class0.is_verb): 
                return None
            res = PartToken._new746(t1, t1, PartToken.ItemType.PREFIX)
            return res
        elif (((t1.is_value("УГОЛОВНОЕ", None) or t1.is_value("КРИМІНАЛЬНА", None))) and t1.next0 is not None and ((t1.next0.is_value("ДЕЛО", None) or t1.next0.is_value("СПРАВА", None)))): 
            t1 = t1.next0
            if (t1.next0 is not None and t1.next0.is_value("ПО", None)): 
                t1 = t1.next0
            return PartToken._new746(t, t1, PartToken.ItemType.PREFIX)
        elif ((((t1.is_value("МОТИВИРОВОЧНЫЙ", None) or t1.is_value("МОТИВУВАЛЬНИЙ", None) or t1.is_value("РЕЗОЛЮТИВНЫЙ", None)) or t1.is_value("РЕЗОЛЮТИВНИЙ", None))) and t1.next0 is not None and ((t1.next0.is_value("ЧАСТЬ", None) or t1.next0.is_value("ЧАСТИНА", None)))): 
            rr = PartToken._new746(t1, t1.next0, PartToken.ItemType.PART)
            rr.values.append(PartToken.PartValue._new965(t1, t1, ("мотивировочная" if t1.is_value("МОТИВИРОВОЧНЫЙ", None) or t1.is_value("МОТИВУВАЛЬНИЙ", None) else "резолютивная")))
            return rr
        if (res is None): 
            return None
        if (ignore_number): 
            return res
        if (res.is_newline_after): 
            if (res.chars.is_all_upper): 
                return None
        if (t1.next0 is not None and t1.next0.is_char('.')): 
            if (not t1.next0.is_newline_after or (t1.length_char < 3)): 
                t1 = t1.next0
        t1 = t1.next0
        if (t1 is None): 
            return None
        if (res.typ == PartToken.ItemType.CLAUSE and t1.is_value("СТ", None)): 
            t1 = t1.next0
            if (t1 is not None and t1.is_char('.')): 
                t1 = t1.next0
        elif (res.typ == PartToken.ItemType.PART and t1.is_value("Ч", None)): 
            t1 = t1.next0
            if (t1 is not None and t1.is_char('.')): 
                t1 = t1.next0
        elif (res.typ == PartToken.ItemType.ITEM and t1.is_value("П", None)): 
            t1 = t1.next0
            if (t1 is not None and t1.is_char('.')): 
                t1 = t1.next0
            res.alt_typ = PartToken.ItemType.SUBITEM
        if (t1 is None): 
            return None
        if (res.typ == PartToken.ItemType.CLAUSE and isinstance(t1.get_referent(), DecreeReferent) and t1.next0 is not None): 
            res.decree = (t1.get_referent() if isinstance(t1.get_referent(), DecreeReferent) else None)
            t1 = t1.next0
        ttn = MiscHelper.check_number_prefix(t1)
        first_num_prefix = None
        if (ttn is not None): 
            first_num_prefix = (t1 if isinstance(t1, TextToken) else None)
            t1 = ttn
        if (t1 is None): 
            return None
        res.end_token = t1
        and0 = False
        ntyp = NumberSpellingType.DIGIT
        tt1 = t1
        while t1 is not None:
            if (t1.whitespaces_before_count > 15): 
                break
            if (t1 != tt1 and t1.is_newline_before): 
                break
            if (ttn is not None): 
                ttn = MiscHelper.check_number_prefix(t1)
                if (ttn is not None): 
                    t1 = ttn
            if (BracketHelper.can_be_start_of_sequence(t1, False, False)): 
                br = BracketHelper.try_parse(t1, BracketParseAttr.NO, 100)
                if (br is None): 
                    break
                ok = True
                newp = None
                ttt = t1.next0
                first_pass2645 = True
                while True:
                    if first_pass2645: first_pass2645 = False
                    else: ttt = ttt.next0
                    if (not (ttt is not None)): break
                    if (ttt.end_char > br.end_token.previous.end_char): 
                        break
                    if (ttt.is_char(',')): 
                        continue
                    if (isinstance(ttt, NumberToken)): 
                        if ((ttt if isinstance(ttt, NumberToken) else None).value == 0): 
                            ok = False
                            break
                        if (newp is None): 
                            newp = list()
                        newp.append(PartToken.PartValue._new965(ttt, ttt, str((ttt if isinstance(ttt, NumberToken) else None).value)))
                        continue
                    to = (ttt if isinstance(ttt, TextToken) else None)
                    if (to is None): 
                        ok = False
                        break
                    if ((res.typ != PartToken.ItemType.ITEM and res.typ != PartToken.ItemType.SUBITEM and res.typ != PartToken.ItemType.INDENTION) and res.typ != PartToken.ItemType.SUBINDENTION): 
                        ok = False
                        break
                    if (not to.chars.is_letter or to.length_char != 1): 
                        ok = False
                        break
                    if (newp is None): 
                        newp = list()
                    pv = PartToken.PartValue._new965(ttt, ttt, to.term)
                    if (BracketHelper.can_be_start_of_sequence(ttt.previous, False, False)): 
                        pv.begin_token = ttt.previous
                    if (BracketHelper.can_be_end_of_sequence(ttt.next0, False, None, False)): 
                        pv.end_token = ttt.next0
                    newp.append(pv)
                if (newp is None or not ok): 
                    break
                res.values.extend(newp)
                res.end_token = br.end_token
                t1 = br.end_token.next0
                if (and0): 
                    break
                if (t1 is not None and t1.is_hiphen and BracketHelper.can_be_start_of_sequence(t1.next0, False, False)): 
                    br1 = BracketHelper.try_parse(t1.next0, BracketParseAttr.NO, 100)
                    if ((br1 is not None and isinstance(t1.next0.next0, TextToken) and t1.next0.next0.length_char == 1) and t1.next0.next0.next0 == br1.end_token): 
                        res.values.append(PartToken.PartValue._new965(br1.begin_token, br1.end_token, (t1.next0.next0 if isinstance(t1.next0.next0, TextToken) else None).term))
                        res.end_token = br1.end_token
                        t1 = br1.end_token.next0
                continue
            if ((isinstance(t1, TextToken) and t1.length_char == 1 and t1.chars.is_letter) and len(res.values) == 0): 
                if (t1.chars.is_all_upper and res.typ == PartToken.ItemType.SUBPROGRAM): 
                    res.values.append(PartToken.PartValue._new965(t1, t1, (t1 if isinstance(t1, TextToken) else None).term))
                    res.end_token = t1
                    return res
                ok = True
                lev = 0
                ttt = t1.previous
                while ttt is not None: 
                    if (ttt.is_newline_after): 
                        break
                    if (ttt.is_char('(')): 
                        lev -= 1
                        if (lev < 0): 
                            ok = False
                            break
                    elif (ttt.is_char(')')): 
                        lev += 1
                    ttt = ttt.previous
                if (ok and t1.next0 is not None and t1.next0.is_char(')')): 
                    res.values.append(PartToken.PartValue._new965(t1, t1.next0, (t1 if isinstance(t1, TextToken) else None).term))
                    res.end_token = t1.next0
                    t1 = t1.next0.next0
                    continue
                if (((ok and t1.next0 is not None and t1.next0.is_char('.')) and not t1.next0.is_whitespace_after and isinstance(t1.next0.next0, NumberToken)) and t1.next0.next0.next0 is not None and t1.next0.next0.next0.is_char(')')): 
                    res.values.append(PartToken.PartValue._new965(t1, t1.next0.next0.next0, "{0}.{1}".format((t1 if isinstance(t1, TextToken) else None).term, (t1.next0.next0 if isinstance(t1.next0.next0, NumberToken) else None).value)))
                    res.end_token = t1.next0.next0.next0
                    t1 = res.end_token.next0
                    continue
            pref_to = None
            if (len(res.values) > 0 and not ((isinstance(t1, NumberToken))) and first_num_prefix is not None): 
                ttn = MiscHelper.check_number_prefix(t1)
                if (ttn is not None): 
                    pref_to = t1
                    t1 = ttn
            if (isinstance(t1, NumberToken)): 
                tt0 = Utils.ifNotNull(pref_to, t1)
                if (len(res.values) > 0): 
                    if (res.values[0].int_value == 0 and not res.values[0].value[0].isdigit()): 
                        break
                    if ((t1 if isinstance(t1, NumberToken) else None).typ != ntyp): 
                        break
                ntyp = (t1 if isinstance(t1, NumberToken) else None).typ
                val = PartToken.PartValue._new965(tt0, t1, str((t1 if isinstance(t1, NumberToken) else None).value))
                val.correct_value()
                res.values.append(val)
                res.end_token = val.end_token
                t1 = res.end_token.next0
                if (and0): 
                    break
                continue
            nt = NumberHelper.try_parse_roman(t1)
            if (nt is not None): 
                pv = PartToken.PartValue._new965(t1, nt.end_token, str(nt.value))
                res.values.append(pv)
                pv.correct_value()
                res.end_token = pv.end_token
                t1 = res.end_token.next0
                continue
            if ((t1 == tt1 and ((res.typ == PartToken.ItemType.APPENDIX or res.typ == PartToken.ItemType.ADDAGREE)) and t1.is_value("К", None)) and t1.next0 is not None and isinstance(t1.next0.get_referent(), DecreeReferent)): 
                res.values.append(PartToken.PartValue._new965(t1, t1, ""))
                break
            if (res.typ == PartToken.ItemType.ADDAGREE and first_num_prefix is not None and len(res.values) == 0): 
                ddd = DecreeToken.try_attach(first_num_prefix, None, False)
                if (ddd is not None and ddd.typ == DecreeToken.ItemType.NUMBER and ddd.value is not None): 
                    res.values.append(PartToken.PartValue._new965(t1, ddd.end_token, ddd.value))
                    res.end_token = ddd.end_token
                    t1 = res.end_token
                    break
            if (len(res.values) == 0): 
                break
            if (t1.is_char_of(",.")): 
                if (t1.is_newline_after and t1.is_char('.')): 
                    break
                t1 = t1.next0
                continue
            if (t1.is_hiphen and res.values[len(res.values) - 1].value.find('.') > 0): 
                t1 = t1.next0
                continue
            if (t1.is_and or t1.is_or): 
                t1 = t1.next0
                and0 = True
                continue
            if (t1.is_hiphen): 
                if (not ((isinstance(t1.next0, NumberToken)))): 
                    break
                min0 = res.values[len(res.values) - 1].int_value
                if (min0 == 0): 
                    break
                max0 = (t1.next0 if isinstance(t1.next0, NumberToken) else None).value
                if (max0 < min0): 
                    break
                if ((max0 - min0) > 200): 
                    break
                val = PartToken.PartValue._new965(t1.next0, t1.next0, str(max0))
                val.correct_value()
                res.values.append(val)
                res.end_token = val.end_token
                t1 = res.end_token.next0
                continue
            break
        if (len(res.values) == 0 and not res.is_newline_after and BracketHelper.can_be_start_of_sequence(res.end_token, True, False)): 
            lev = PartToken._get_rank(res.typ)
            if (lev > 0 and (lev < PartToken._get_rank(PartToken.ItemType.CLAUSE))): 
                br = BracketHelper.try_parse(res.end_token, BracketParseAttr.NO, 100)
                if (br is not None): 
                    res.name = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                    res.end_token = br.end_token
        if (len(res.values) == 0 and res.name is None): 
            if (not ignore_number and res.typ != PartToken.ItemType.PREAMBLE and res.typ != PartToken.ItemType.SUBPROGRAM): 
                return None
            if (res.begin_token != res.end_token): 
                res.end_token = res.end_token.previous
        return res
    
    @staticmethod
    def __create_part_typ0(t1 : 'Token', prev : 'PartToken') -> 'PartToken':
        inoutarg985 = RefOutArgWrapper(None)
        pt = PartToken.__create_part_typ(t1, prev, inoutarg985)
        is_short = inoutarg985.value
        if (pt is None): 
            return None
        if ((is_short and not pt.end_token.is_whitespace_after and pt.end_token.next0 is not None) and pt.end_token.next0.is_char('.')): 
            if (not pt.end_token.next0.is_newline_after): 
                pt.end_token = pt.end_token.next0
        return pt
    
    @staticmethod
    def __create_part_typ(t1 : 'Token', prev : 'PartToken', is_short : bool) -> 'PartToken':
        is_short.value = False
        if (t1 is None): 
            return None
        if (t1.is_value("ЧАСТЬ", "ЧАСТИНА")): 
            return PartToken._new746(t1, t1, PartToken.ItemType.PART)
        if (t1.is_value("Ч", None)): 
            is_short.value = True
            return PartToken._new746(t1, t1, PartToken.ItemType.PART)
        if (t1.is_value("ГЛАВА", None) or t1.is_value("ГЛ", None)): 
            is_short.value = t1.length_char == 2
            return PartToken._new746(t1, t1, PartToken.ItemType.CHAPTER)
        if (t1.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК") or t1.is_value("ПРИЛ", None)): 
            if ((t1.is_newline_before and t1.length_char > 6 and t1.next0 is not None) and t1.next0.is_char(':')): 
                return None
            is_short.value = (t1.length_char < 5)
            return PartToken._new746(t1, t1, PartToken.ItemType.APPENDIX)
        if (t1.is_value("ПРИМЕЧАНИЕ", "ПРИМІТКА") or t1.is_value("ПРИМ", None)): 
            is_short.value = (t1.length_char < 5)
            return PartToken._new746(t1, t1, PartToken.ItemType.NOTICE)
        if (t1.is_value("СТАТЬЯ", "СТАТТЯ") or t1.is_value("СТ", None)): 
            is_short.value = (t1.length_char < 3)
            return PartToken._new746(t1, t1, PartToken.ItemType.CLAUSE)
        if (t1.is_value("ПУНКТ", None) or t1.is_value("П", None) or t1.is_value("ПП", None)): 
            is_short.value = (t1.length_char < 3)
            return PartToken._new992(t1, t1, PartToken.ItemType.ITEM, (PartToken.ItemType.SUBITEM if t1.is_value("ПП", None) else PartToken.ItemType.UNDEFINED))
        if (t1.is_value("ПОДПУНКТ", "ПІДПУНКТ")): 
            return PartToken._new746(t1, t1, PartToken.ItemType.SUBITEM)
        if (t1.is_value("ПРЕАМБУЛА", None)): 
            return PartToken._new746(t1, t1, PartToken.ItemType.PREAMBLE)
        if (t1.is_value("ПОДП", None) or t1.is_value("ПІДП", None)): 
            is_short.value = True
            return PartToken._new746(t1, t1, PartToken.ItemType.SUBITEM)
        if (t1.is_value("РАЗДЕЛ", "РОЗДІЛ") or t1.is_value("РАЗД", None)): 
            is_short.value = (t1.length_char < 5)
            return PartToken._new746(t1, t1, PartToken.ItemType.SECTION)
        if (((t1.is_value("Р", None) or t1.is_value("P", None))) and t1.next0 is not None and t1.next0.is_char('.')): 
            if (prev is not None): 
                if (prev.typ == PartToken.ItemType.ITEM or prev.typ == PartToken.ItemType.SUBITEM): 
                    is_short.value = True
                    return PartToken._new746(t1, t1.next0, PartToken.ItemType.SECTION)
        if (t1.is_value("ПОДРАЗДЕЛ", "ПІРОЗДІЛ")): 
            return PartToken._new746(t1, t1, PartToken.ItemType.SUBSECTION)
        if (t1.is_value("ПАРАГРАФ", None) or t1.is_value("§", None)): 
            return PartToken._new746(t1, t1, PartToken.ItemType.PARAGRAPH)
        if (t1.is_value("АБЗАЦ", None) or t1.is_value("АБЗ", None)): 
            is_short.value = (t1.length_char < 7)
            return PartToken._new746(t1, t1, PartToken.ItemType.INDENTION)
        if (t1.is_value("СТРАНИЦА", "СТОРІНКА") or t1.is_value("СТР", "СТОР")): 
            is_short.value = (t1.length_char < 7)
            return PartToken._new746(t1, t1, PartToken.ItemType.PAGE)
        if (t1.is_value("ПОДАБЗАЦ", "ПІДАБЗАЦ") or t1.is_value("ПОДАБЗ", "ПІДАБЗ")): 
            return PartToken._new746(t1, t1, PartToken.ItemType.SUBINDENTION)
        if (t1.is_value("ПОДПАРАГРАФ", "ПІДПАРАГРАФ")): 
            return PartToken._new746(t1, t1, PartToken.ItemType.SUBPARAGRAPH)
        if (t1.is_value("ПОДПРОГРАММА", "ПІДПРОГРАМА")): 
            return PartToken._new746(t1, t1, PartToken.ItemType.SUBPROGRAM)
        if (t1.is_value("ДОПСОГЛАШЕНИЕ", None)): 
            return PartToken._new746(t1, t1, PartToken.ItemType.ADDAGREE)
        if (((t1.is_value("ДОП", None) or t1.is_value("ДОПОЛНИТЕЛЬНЫЙ", "ДОДАТКОВА"))) and t1.next0 is not None): 
            tt = t1.next0
            if (tt.is_char('.') and tt.next0 is not None): 
                tt = tt.next0
            if (tt.is_value("СОГЛАШЕНИЕ", "УГОДА")): 
                return PartToken._new746(t1, tt, PartToken.ItemType.ADDAGREE)
        return None
    
    @staticmethod
    def try_attach_list(t : 'Token', in_bracket : bool=False, max_count : int=40) -> typing.List['PartToken']:
        """ Привязать примитивы в контейнере с указанной позиции
        
        Returns:
            typing.List[PartToken]: Список примитивов
        """
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.NumberToken import NumberToken
        
        p = PartToken.try_attach(t, None, in_bracket, False)
        if (p is None): 
            return None
        res = list()
        res.append(p)
        if (p.is_newline_after and p.is_newline_before): 
            if (not p.begin_token.chars.is_all_lower): 
                return res
        tt = p.end_token.next0
        while tt is not None:
            if (tt.whitespaces_before_count > 15): 
                if (tt.previous is not None and tt.previous.is_comma_and): 
                    pass
                else: 
                    break
            if (max_count > 0 and len(res) >= max_count): 
                break
            delim = False
            if (((tt.is_char_of(",;.") or tt.is_and or tt.is_or)) and tt.next0 is not None): 
                if (tt.is_char_of(";.")): 
                    res[len(res) - 1].has_terminator = True
                else: 
                    res[len(res) - 1].delim_after = True
                    if ((tt.next0 is not None and tt.next0.is_value("А", None) and tt.next0.next0 is not None) and tt.next0.next0.is_value("ТАКЖЕ", "ТАКОЖ")): 
                        tt = tt.next0.next0
                tt = tt.next0
                delim = True
            if (tt is None): 
                break
            if (tt.is_char('(')): 
                br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                if (br is not None): 
                    li = PartToken.try_attach_list(tt.next0, True, 40)
                    if (li is not None and len(li) > 0): 
                        if (li[0].typ == PartToken.ItemType.PARAGRAPH or li[0].typ == PartToken.ItemType.PART or li[0].typ == PartToken.ItemType.ITEM): 
                            if (li[len(li) - 1].end_token.next0 == br.end_token): 
                                if (len(p.values) > 1): 
                                    for ii in range(1, len(p.values), 1):
                                        pp = PartToken._new746(p.values[ii].begin_token, (p.end_token if ii == (len(p.values) - 1) else p.values[ii].end_token), p.typ)
                                        pp.values.append(p.values[ii])
                                        res.append(pp)
                                    if (p.values[1].begin_token.previous is not None and p.values[1].begin_token.previous.end_char >= p.begin_token.begin_char): 
                                        p.end_token = p.values[1].begin_token.previous
                                    del p.values[1:1+len(p.values) - 1]
                                res.extend(li)
                                li[len(li) - 1].end_token = br.end_token
                                tt = br.end_token.next0
                                continue
            p0 = PartToken.try_attach(tt, p, in_bracket, False)
            if (p0 is None and ((tt.is_value("В", None) or tt.is_value("К", None) or tt.is_value("ДО", None)))): 
                p0 = PartToken.try_attach(tt.next0, p, in_bracket, False)
            if (p0 is None): 
                if (BracketHelper.is_bracket(tt, False)): 
                    br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        p0 = PartToken.try_attach(br.end_token.next0, None, False, False)
                        if (p0 is not None and p0.typ != PartToken.ItemType.PREFIX and len(p0.values) > 0): 
                            res[len(res) - 1].end_token = br.end_token
                            res[len(res) - 1].name = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                            p = p0
                            res.append(p)
                            tt = p.end_token.next0
                            continue
                if (tt.is_newline_before): 
                    if (len(res) == 1 and res[0].is_newline_before): 
                        break
                    if (tt.previous is not None and tt.previous.is_comma_and): 
                        pass
                    else: 
                        break
                if (isinstance(tt, NumberToken) and delim): 
                    p0 = None
                    if (p.typ == PartToken.ItemType.CLAUSE or in_bracket): 
                        p0 = PartToken._new746(tt, tt, PartToken.ItemType.CLAUSE)
                    elif (len(res) > 1 and res[len(res) - 2].typ == PartToken.ItemType.CLAUSE and res[len(res) - 1].typ == PartToken.ItemType.PART): 
                        p0 = PartToken._new746(tt, tt, PartToken.ItemType.CLAUSE)
                    elif ((len(res) > 2 and res[len(res) - 3].typ == PartToken.ItemType.CLAUSE and res[len(res) - 2].typ == PartToken.ItemType.PART) and res[len(res) - 1].typ == PartToken.ItemType.ITEM): 
                        p0 = PartToken._new746(tt, tt, PartToken.ItemType.CLAUSE)
                    elif (len(res) > 0 and len(res[len(res) - 1].values) > 0 and "." in res[len(res) - 1].values[0].value): 
                        p0 = PartToken._new746(tt, tt, res[len(res) - 1].typ)
                    if (p0 is None): 
                        break
                    vv = PartToken.PartValue._new965(tt, tt, str((tt if isinstance(tt, NumberToken) else None).value))
                    p0.values.append(vv)
                    vv.correct_value()
                    p0.end_token = vv.end_token
                    tt = p0.end_token.next0
                    if (tt is not None and tt.is_hiphen and ((isinstance(tt.next0, NumberToken)))): 
                        tt = tt.next0
                        vv = PartToken.PartValue._new965(tt, tt, str((tt if isinstance(tt, NumberToken) else None).value))
                        vv.correct_value()
                        p0.values.append(vv)
                        p0.end_token = vv.end_token
                        tt = p0.end_token.next0
            if (p0 is None): 
                break
            if (p0.is_newline_before and len(res) == 1 and res[0].is_newline_before): 
                break
            if (p0.typ == PartToken.ItemType.ITEM and p.typ == PartToken.ItemType.ITEM): 
                if (p0.alt_typ == PartToken.ItemType.UNDEFINED and p.alt_typ == PartToken.ItemType.SUBITEM): 
                    p.typ = PartToken.ItemType.SUBITEM
                    p.alt_typ = PartToken.ItemType.UNDEFINED
                elif (p.alt_typ == PartToken.ItemType.UNDEFINED and p0.alt_typ == PartToken.ItemType.SUBITEM): 
                    p0.typ = PartToken.ItemType.SUBITEM
                    p0.alt_typ = PartToken.ItemType.UNDEFINED
            p = p0
            res.append(p)
            tt = p.end_token.next0
        i = 0
        first_pass2646 = True
        while True:
            if first_pass2646: first_pass2646 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].typ == PartToken.ItemType.PART and res[i + 1].typ == PartToken.ItemType.PART and len(res[i].values) > 1): 
                v1 = res[i].values[len(res[i].values) - 2].int_value
                v2 = res[i].values[len(res[i].values) - 1].int_value
                if (v1 == 0 or v2 == 0): 
                    continue
                if ((v2 - v1) < 10): 
                    continue
                pt = PartToken._new746(res[i].end_token, res[i].end_token, PartToken.ItemType.CLAUSE)
                pt.values.append(PartToken.PartValue._new965(res[i].end_token, res[i].end_token, str(v2)))
                del res[i].values[len(res[i].values) - 1]
                if (res[i].end_token != res[i].begin_token): 
                    res[i].end_token = res[i].end_token.previous
                res.insert(i + 1, pt)
        if ((len(res) == 1 and res[0].typ == PartToken.ItemType.SUBPROGRAM and res[0].end_token.next0 is not None) and res[0].end_token.next0.is_char('.')): 
            res[0].end_token = res[0].end_token.next0
        for i in range(len(res) - 1, -1, -1):
            p = res[i]
            if (p.is_newline_after and p.is_newline_before and p.typ != PartToken.ItemType.SUBPROGRAM): 
                del res[i:i+len(res) - i]
                continue
            if (((i == 0 and p.is_newline_before and p.has_terminator) and p.end_token.next0 is not None and p.end_token.next0.is_char('.')) and MiscHelper.can_be_start_of_sentence(p.end_token.next0.next0)): 
                del res[i]
                continue
        return (None if len(res) == 0 else res)
    
    def can_be_next_narrow(self, p : 'PartToken') -> bool:
        if (self.typ == p.typ): 
            if (self.typ != PartToken.ItemType.SUBITEM): 
                return False
            if (p.values is not None and len(p.values) > 0 and p.values[0].int_value == 0): 
                if (self.values is not None and len(self.values) > 0 and self.values[0].int_value > 0): 
                    return True
            return False
        if (self.typ == PartToken.ItemType.PART or p.typ == PartToken.ItemType.PART): 
            return True
        i1 = PartToken._get_rank(self.typ)
        i2 = PartToken._get_rank(p.typ)
        if (i1 >= 0 and i2 >= 0): 
            return i1 < i2
        return False
    
    @staticmethod
    def is_part_before(t0 : 'Token') -> bool:
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.TextToken import TextToken
        if (t0 is None): 
            return False
        i = 0
        tt = t0.previous
        while tt is not None: 
            if (tt.is_newline_after or ((isinstance(tt, ReferentToken)))): 
                break
            else: 
                st = PartToken.try_attach(tt, None, False, False)
                if (st is not None): 
                    if (st.end_token.next0 == t0): 
                        return True
                    break
                if (isinstance(tt, TextToken) and tt.chars.is_letter): 
                    i += 1
                    if ((i) > 2): 
                        break
            tt = tt.previous
        return False
    
    @staticmethod
    def _get_rank(t : 'ItemType') -> int:
        if (t == PartToken.ItemType.DOCPART): 
            return 1
        if (t == PartToken.ItemType.APPENDIX): 
            return 1
        if (t == PartToken.ItemType.SECTION): 
            return 2
        if (t == PartToken.ItemType.SUBPROGRAM): 
            return 2
        if (t == PartToken.ItemType.SUBSECTION): 
            return 3
        if (t == PartToken.ItemType.CHAPTER): 
            return 4
        if (t == PartToken.ItemType.PREAMBLE): 
            return 5
        if (t == PartToken.ItemType.PARAGRAPH): 
            return 5
        if (t == PartToken.ItemType.SUBPARAGRAPH): 
            return 6
        if (t == PartToken.ItemType.PAGE): 
            return 6
        if (t == PartToken.ItemType.CLAUSE): 
            return 7
        if (t == PartToken.ItemType.PART): 
            return 8
        if (t == PartToken.ItemType.NOTICE): 
            return 8
        if (t == PartToken.ItemType.ITEM): 
            return 9
        if (t == PartToken.ItemType.SUBITEM): 
            return 10
        if (t == PartToken.ItemType.INDENTION): 
            return 11
        if (t == PartToken.ItemType.SUBINDENTION): 
            return 12
        return 0
    
    @staticmethod
    def _get_attr_name_by_typ(typ_ : 'ItemType') -> str:
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        if (typ_ == PartToken.ItemType.CHAPTER): 
            return DecreePartReferent.ATTR_CHAPTER
        if (typ_ == PartToken.ItemType.APPENDIX): 
            return DecreePartReferent.ATTR_APPENDIX
        if (typ_ == PartToken.ItemType.CLAUSE): 
            return DecreePartReferent.ATTR_CLAUSE
        if (typ_ == PartToken.ItemType.INDENTION): 
            return DecreePartReferent.ATTR_INDENTION
        if (typ_ == PartToken.ItemType.ITEM): 
            return DecreePartReferent.ATTR_ITEM
        if (typ_ == PartToken.ItemType.PARAGRAPH): 
            return DecreePartReferent.ATTR_PARAGRAPH
        if (typ_ == PartToken.ItemType.SUBPARAGRAPH): 
            return DecreePartReferent.ATTR_SUBPARAGRAPH
        if (typ_ == PartToken.ItemType.PART): 
            return DecreePartReferent.ATTR_PART
        if (typ_ == PartToken.ItemType.SECTION): 
            return DecreePartReferent.ATTR_SECTION
        if (typ_ == PartToken.ItemType.SUBSECTION): 
            return DecreePartReferent.ATTR_SUBSECTION
        if (typ_ == PartToken.ItemType.SUBINDENTION): 
            return DecreePartReferent.ATTR_SUBINDENTION
        if (typ_ == PartToken.ItemType.SUBITEM): 
            return DecreePartReferent.ATTR_SUBITEM
        if (typ_ == PartToken.ItemType.PREAMBLE): 
            return DecreePartReferent.ATTR_PREAMBLE
        if (typ_ == PartToken.ItemType.NOTICE): 
            return DecreePartReferent.ATTR_NOTICE
        if (typ_ == PartToken.ItemType.SUBPROGRAM): 
            return DecreePartReferent.ATTR_SUBPROGRAM
        if (typ_ == PartToken.ItemType.ADDAGREE): 
            return DecreePartReferent.ATTR_ADDAGREE
        if (typ_ == PartToken.ItemType.DOCPART): 
            return DecreePartReferent.ATTR_DOCPART
        if (typ_ == PartToken.ItemType.PAGE): 
            return DecreePartReferent.ATTR_PAGE
        return None
    
    @staticmethod
    def _get_instr_kind_by_typ(typ_ : 'ItemType') -> 'InstrumentKind':
        if (typ_ == PartToken.ItemType.CHAPTER): 
            return InstrumentKind.CHAPTER
        if (typ_ == PartToken.ItemType.APPENDIX): 
            return InstrumentKind.APPENDIX
        if (typ_ == PartToken.ItemType.CLAUSE): 
            return InstrumentKind.CLAUSE
        if (typ_ == PartToken.ItemType.INDENTION): 
            return InstrumentKind.INDENTION
        if (typ_ == PartToken.ItemType.ITEM): 
            return InstrumentKind.ITEM
        if (typ_ == PartToken.ItemType.PARAGRAPH): 
            return InstrumentKind.PARAGRAPH
        if (typ_ == PartToken.ItemType.SUBPARAGRAPH): 
            return InstrumentKind.SUBPARAGRAPH
        if (typ_ == PartToken.ItemType.PART): 
            return InstrumentKind.CLAUSEPART
        if (typ_ == PartToken.ItemType.SECTION): 
            return InstrumentKind.SECTION
        if (typ_ == PartToken.ItemType.SUBSECTION): 
            return InstrumentKind.SUBSECTION
        if (typ_ == PartToken.ItemType.SUBITEM): 
            return InstrumentKind.SUBITEM
        if (typ_ == PartToken.ItemType.PREAMBLE): 
            return InstrumentKind.PREAMBLE
        if (typ_ == PartToken.ItemType.NOTICE): 
            return InstrumentKind.NOTICE
        if (typ_ == PartToken.ItemType.DOCPART): 
            return InstrumentKind.DOCPART
        return InstrumentKind.UNDEFINED
    
    @staticmethod
    def _get_type_by_attr_name(name_ : str) -> 'ItemType':
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        if (name_ == DecreePartReferent.ATTR_CHAPTER): 
            return PartToken.ItemType.CHAPTER
        if (name_ == DecreePartReferent.ATTR_APPENDIX): 
            return PartToken.ItemType.APPENDIX
        if (name_ == DecreePartReferent.ATTR_CLAUSE): 
            return PartToken.ItemType.CLAUSE
        if (name_ == DecreePartReferent.ATTR_INDENTION): 
            return PartToken.ItemType.INDENTION
        if (name_ == DecreePartReferent.ATTR_ITEM): 
            return PartToken.ItemType.ITEM
        if (name_ == DecreePartReferent.ATTR_PARAGRAPH): 
            return PartToken.ItemType.PARAGRAPH
        if (name_ == DecreePartReferent.ATTR_SUBPARAGRAPH): 
            return PartToken.ItemType.SUBPARAGRAPH
        if (name_ == DecreePartReferent.ATTR_PART): 
            return PartToken.ItemType.PART
        if (name_ == DecreePartReferent.ATTR_SECTION): 
            return PartToken.ItemType.SECTION
        if (name_ == DecreePartReferent.ATTR_SUBSECTION): 
            return PartToken.ItemType.SUBSECTION
        if (name_ == DecreePartReferent.ATTR_SUBINDENTION): 
            return PartToken.ItemType.SUBINDENTION
        if (name_ == DecreePartReferent.ATTR_SUBITEM): 
            return PartToken.ItemType.SUBITEM
        if (name_ == DecreePartReferent.ATTR_NOTICE): 
            return PartToken.ItemType.NOTICE
        if (name_ == DecreePartReferent.ATTR_PREAMBLE): 
            return PartToken.ItemType.PREAMBLE
        if (name_ == DecreePartReferent.ATTR_SUBPROGRAM): 
            return PartToken.ItemType.SUBPROGRAM
        if (name_ == DecreePartReferent.ATTR_ADDAGREE): 
            return PartToken.ItemType.ADDAGREE
        if (name_ == DecreePartReferent.ATTR_DOCPART): 
            return PartToken.ItemType.DOCPART
        return PartToken.ItemType.PREFIX
    
    @staticmethod
    def try_create_between(p1 : 'DecreePartReferent', p2 : 'DecreePartReferent') -> typing.List['DecreePartReferent']:
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        not_eq_attr = None
        val1 = None
        val2 = None
        for s1 in p1.slots: 
            if (p2.find_slot(s1.type_name, s1.value, True) is not None): 
                continue
            else: 
                if (not_eq_attr is not None): 
                    return None
                val2 = p2.get_string_value(s1.type_name)
                if (val2 is None): 
                    return None
                not_eq_attr = s1.type_name
                val1 = (s1.value if isinstance(s1.value, str) else None)
        if (val1 is None or val2 is None): 
            return None
        diap = NumberingHelper.create_diap(val1, val2)
        if (diap is None or (len(diap) < 3)): 
            return None
        res = list()
        i = 1
        while i < (len(diap) - 1): 
            dpr = DecreePartReferent()
            for s in p1.slots: 
                val = s.value
                if (s.type_name == not_eq_attr): 
                    val = diap[i]
                dpr.add_slot(s.type_name, val, False, 0)
            res.append(dpr)
            i += 1
        return res
    
    @staticmethod
    def get_number(str0 : str) -> int:
        if (Utils.isNullOrEmpty(str0)): 
            return 0
        inoutarg1020 = RefOutArgWrapper(None)
        inoutres1021 = Utils.tryParseInt(str0, inoutarg1020)
        i = inoutarg1020.value
        if (inoutres1021): 
            return i
        if (not str0[0].isalpha()): 
            return 0
        ch = str0[0].upper()
        if (ord(ch) < 0x80): 
            i = ((ord(ch) - ord('A')) + 1)
            if ((ch == 'Z' and len(str0) > 2 and str0[1] == '.') and str0[2].isdigit()): 
                inoutarg1016 = RefOutArgWrapper(None)
                inoutres1017 = Utils.tryParseInt(str0[2 : ], inoutarg1016)
                n = inoutarg1016.value
                if (inoutres1017): 
                    i += n
        elif (LanguageHelper.is_cyrillic_char(ch)): 
            i = PartToken.__ru_nums.find(ch)
            if (i < 0): 
                return 0
            i += 1
            if ((ch == 'Я' and len(str0) > 2 and str0[1] == '.') and str0[2].isdigit()): 
                inoutarg1018 = RefOutArgWrapper(None)
                inoutres1019 = Utils.tryParseInt(str0[2 : ], inoutarg1018)
                n = inoutarg1018.value
                if (inoutres1019): 
                    i += n
        if (i < 0): 
            return 0
        return i
    
    __ru_nums = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ"

    
    @staticmethod
    def _new746(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType') -> 'PartToken':
        res = PartToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new968(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : bool) -> 'PartToken':
        res = PartToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt = _arg4
        return res
    
    @staticmethod
    def _new992(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'ItemType') -> 'PartToken':
        res = PartToken(_arg1, _arg2)
        res.typ = _arg3
        res.alt_typ = _arg4
        return res