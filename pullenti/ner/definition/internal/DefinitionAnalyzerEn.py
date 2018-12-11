﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.definition.DefinitionKind import DefinitionKind


class DefinitionAnalyzerEn:
    
    @staticmethod
    def process(kit : 'AnalysisKit', ad : 'AnalyzerData') -> None:
        from pullenti.ner.core.MiscHelper import MiscHelper
        t = kit.first_token
        first_pass2883 = True
        while True:
            if first_pass2883: first_pass2883 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not MiscHelper.canBeStartOfSentence(t)): 
                continue
            rt = DefinitionAnalyzerEn.__tryParseThesis(t)
            if (rt is None): 
                continue
            rt.referent = ad.registerReferent(rt.referent)
            kit.embedToken(rt)
            t = (rt)
    
    @staticmethod
    def __tryParseThesis(t : 'Token') -> 'ReferentToken':
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.MetaToken import MetaToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.NounPhraseToken import NounPhraseToken
        from pullenti.ner.definition.DefinitionReferent import DefinitionReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (t is None): 
            return None
        t0 = t
        tt = t
        mc = tt.getMorphClassInDictionary()
        preamb = None
        if (mc.is_conjunction): 
            return None
        if (t.isValue("LET", None)): 
            return None
        if (mc.is_preposition or mc.is_misc or mc.is_adverb): 
            if (not MiscHelper.isEngArticle(tt)): 
                tt = tt.next0_
                first_pass2884 = True
                while True:
                    if first_pass2884: first_pass2884 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.is_comma): 
                        break
                    if (tt.isChar('(')): 
                        br = BracketHelper.tryParse(tt, BracketParseAttr.NO, 100)
                        if (br is not None): 
                            tt = br.end_token
                            continue
                    if (MiscHelper.canBeStartOfSentence(tt)): 
                        break
                    npt0 = NounPhraseHelper.tryParse(tt, Utils.valToEnum((NounPhraseParseAttr.PARSENUMERICASADJECTIVE) | (NounPhraseParseAttr.REFERENTCANBENOUN), NounPhraseParseAttr), 0)
                    if (npt0 is not None): 
                        tt = npt0.end_token
                        continue
                    if (tt.getMorphClassInDictionary().is_verb): 
                        break
                if (tt is None or not tt.is_comma or tt.next0_ is None): 
                    return None
                preamb = MetaToken(t0, tt.previous)
                tt = tt.next0_
        t1 = tt
        mc = tt.getMorphClassInDictionary()
        npt = NounPhraseHelper.tryParse(tt, Utils.valToEnum((NounPhraseParseAttr.PARSENUMERICASADJECTIVE) | (NounPhraseParseAttr.REFERENTCANBENOUN) | (NounPhraseParseAttr.PARSEADVERBS), NounPhraseParseAttr), 0)
        if (npt is None and (isinstance(tt, TextToken))): 
            if (tt.chars.is_all_upper): 
                npt = NounPhraseToken(tt, tt)
            elif (not tt.chars.is_all_lower): 
                if (mc.is_proper or preamb is not None): 
                    npt = NounPhraseToken(tt, tt)
        if (npt is None): 
            return None
        if (mc.is_personal_pronoun): 
            return None
        t2 = npt.end_token.next0_
        if (t2 is None or MiscHelper.canBeStartOfSentence(t2) or not ((isinstance(t2, TextToken)))): 
            return None
        if (not t2.getMorphClassInDictionary().is_verb): 
            return None
        t3 = t2
        tt = t2.next0_
        while tt is not None: 
            if (not tt.getMorphClassInDictionary().is_verb): 
                break
            tt = tt.next0_
        first_pass2885 = True
        while True:
            if first_pass2885: first_pass2885 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.next0_ is None): 
                t3 = tt
                break
            if (tt.isCharOf(".;!?")): 
                if (MiscHelper.canBeStartOfSentence(tt.next0_)): 
                    t3 = tt
                    break
            if (not ((isinstance(tt, TextToken)))): 
                continue
            if (BracketHelper.canBeStartOfSequence(tt, False, False)): 
                br = BracketHelper.tryParse(tt, BracketParseAttr.NO, 100)
                if (br is not None): 
                    tt = br.end_token
                    continue
        tt = t3
        if (t3.isCharOf(";.!?")): 
            tt = tt.previous
        txt = MiscHelper.getTextValue(t2, tt, Utils.valToEnum((GetTextAttr.KEEPREGISTER) | (GetTextAttr.KEEPQUOTES), GetTextAttr))
        if (txt is None or (len(txt) < 15)): 
            return None
        if (t0 != t1): 
            tt = t1.previous
            if (tt.is_comma): 
                tt = tt.previous
            txt0 = MiscHelper.getTextValue(t0, tt, Utils.valToEnum((GetTextAttr.KEEPREGISTER) | (GetTextAttr.KEEPQUOTES), GetTextAttr))
            if (txt0 is not None and len(txt0) > 10): 
                if (t0.chars.is_capital_upper): 
                    txt0 = ((str.lower(txt0[0])) + txt0[1:])
                txt = "{0}, {1}".format(txt, txt0)
        tt = t1
        if (MiscHelper.isEngArticle(tt)): 
            tt = tt.next0_
        nam = MiscHelper.getTextValue(tt, t2.previous, GetTextAttr.KEEPQUOTES)
        if (nam.startswith("SO-CALLED")): 
            nam = nam[9:].strip()
        dr = DefinitionReferent()
        dr.kind = DefinitionKind.ASSERTATION
        dr.addSlot(DefinitionReferent.ATTR_TERMIN, nam, False, 0)
        dr.addSlot(DefinitionReferent.ATTR_VALUE, txt, False, 0)
        return ReferentToken(dr, t0, t3)