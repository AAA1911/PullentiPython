﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.morph.MorphGender import MorphGender

from pullenti.ner.person.internal.ResourceHelper import ResourceHelper
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis


class ShortNameHelper:
    
    class ShortnameVar:
        
        def __init__(self) -> None:
            self.name = None
            self.gender = MorphGender.UNDEFINED
        
        def __str__(self) -> str:
            return self.name
    
        
        @staticmethod
        def _new2259(_arg1 : str, _arg2 : 'MorphGender') -> 'ShortnameVar':
            res = ShortNameHelper.ShortnameVar()
            res.name = _arg1
            res.gender = _arg2
            return res
    
    __m_shorts_names = dict()
    
    @staticmethod
    def get_shortnames_for_name(name : str) -> typing.List[str]:
        res = list()
        for kp in ShortNameHelper.__m_shorts_names.items(): 
            for v in kp[1]: 
                if (v.name == name): 
                    if (not kp[0] in res): 
                        res.append(kp[0])
        return res
    
    @staticmethod
    def get_names_for_shortname(shortname : str) -> typing.List['ShortnameVar']:
        res = [ ]
        inoutarg2257 = RefOutArgWrapper(None)
        inoutres2258 = Utils.tryGetValue(ShortNameHelper.__m_shorts_names, shortname, inoutarg2257)
        res = inoutarg2257.value
        if (not inoutres2258): 
            return None
        else: 
            return res
    
    __m_inited = False
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.AnalysisKit import AnalysisKit
        from pullenti.ner.TextToken import TextToken
        if (ShortNameHelper.__m_inited): 
            return
        ShortNameHelper.__m_inited = True
        obj = ResourceHelper.get_string("ShortNames.txt")
        if (obj is not None): 
            kit = AnalysisKit(SourceOfAnalysis(obj))
            t = kit.first_token
            while t is not None: 
                if (t.is_newline_before): 
                    g = (MorphGender.FEMINIE if t.is_value("F", None) else MorphGender.MASCULINE)
                    t = t.next0
                    nam = (t if isinstance(t, TextToken) else None).term
                    shos = list()
                    t = t.next0
                    while t is not None: 
                        if (t.is_newline_before): 
                            break
                        else: 
                            shos.append((t if isinstance(t, TextToken) else None).term)
                        t = t.next0
                    for s in shos: 
                        li = None
                        inoutarg2260 = RefOutArgWrapper(None)
                        inoutres2261 = Utils.tryGetValue(ShortNameHelper.__m_shorts_names, s, inoutarg2260)
                        li = inoutarg2260.value
                        if (not inoutres2261): 
                            li = list()
                            ShortNameHelper.__m_shorts_names[s] = li
                        li.append(ShortNameHelper.ShortnameVar._new2259(nam, g))
                    if (t is None): 
                        break
                    t = t.previous
                t = t.next0