﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.named.NamedEntityKind import NamedEntityKind
from pullenti.ner.business.internal.ResourceHelper import ResourceHelper
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.GetTextAttr import GetTextAttr


class NamedEntityAnalyzer(Analyzer):
    
    ANALYZER_NAME = "NAMEDENTITY"
    
    @property
    def name(self) -> str:
        return NamedEntityAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Мелкие именованные сущности"
    
    @property
    def description(self) -> str:
        return "Планеты, памятники, здания, местоположения, планеты и пр."
    
    def clone(self) -> 'Analyzer':
        return NamedEntityAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        from pullenti.ner.named.internal.MetaNamedEntity import MetaNamedEntity
        return [MetaNamedEntity.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[Utils.enumToString(NamedEntityKind.MONUMENT)] = ResourceHelper.get_bytes("monument.png")
        res[Utils.enumToString(NamedEntityKind.PLANET)] = ResourceHelper.get_bytes("planet.png")
        res[Utils.enumToString(NamedEntityKind.LOCATION)] = ResourceHelper.get_bytes("location.png")
        res[Utils.enumToString(NamedEntityKind.BUILDING)] = ResourceHelper.get_bytes("building.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        from pullenti.ner.named.NamedEntityReferent import NamedEntityReferent
        if (type0_ == NamedEntityReferent.OBJ_TYPENAME): 
            return NamedEntityReferent()
        return None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        from pullenti.ner.geo.GeoReferent import GeoReferent
        return [GeoReferent.OBJ_TYPENAME, "ORGANIZATION", "PERSON"]
    
    @property
    def progress_weight(self) -> int:
        return 3
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
        return AnalyzerDataWithOntology()
    
    def process(self, kit : 'AnalysisKit') -> None:
        from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
        from pullenti.ner.named.internal.NamedItemToken import NamedItemToken
        ad = (kit.get_analyzer_data(self) if isinstance(kit.get_analyzer_data(self), AnalyzerDataWithOntology) else None)
        t = kit.first_token
        first_pass2972 = True
        while True:
            if first_pass2972: first_pass2972 = False
            else: t = t.next0_
            if (not (t is not None)): break
            li = NamedItemToken.try_parse_list(t, ad.local_ontology)
            if (li is None or len(li) == 0): 
                continue
            rt = NamedEntityAnalyzer.__try_attach(li)
            if (rt is not None): 
                rt.referent = ad.register_referent(rt.referent)
                kit.embed_token(rt)
                t = rt
                continue
    
    def _process_referent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        from pullenti.ner.named.internal.NamedItemToken import NamedItemToken
        li = NamedItemToken.try_parse_list(begin, None)
        if (li is None or len(li) == 0): 
            return None
        rt = NamedEntityAnalyzer.__try_attach(li)
        if (rt is None): 
            return None
        rt.data = begin.kit.get_analyzer_data(self)
        return rt
    
    @staticmethod
    def __can_be_ref(ki : 'NamedEntityKind', re : 'Referent') -> bool:
        from pullenti.ner.geo.GeoReferent import GeoReferent
        if (re is None): 
            return False
        if (ki == NamedEntityKind.MONUMENT): 
            if (re.type_name == "PERSON" or re.type_name == "PERSONPROPERTY"): 
                return True
        elif (ki == NamedEntityKind.LOCATION): 
            if (isinstance(re, GeoReferent)): 
                geo_ = (re if isinstance(re, GeoReferent) else None)
                if (geo_.is_region or geo_.is_state): 
                    return True
        elif (ki == NamedEntityKind.BUILDING): 
            if (re.type_name == "ORGANIZATION"): 
                return True
        return False
    
    @staticmethod
    def __try_attach(toks : typing.List['NamedItemToken']) -> 'ReferentToken':
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.named.NamedEntityReferent import NamedEntityReferent
        from pullenti.ner.ReferentToken import ReferentToken
        typ = None
        re = None
        nams = None
        ki = NamedEntityKind.UNDEFINED
        for i in range(len(toks)):
            if (toks[i].type_value is not None): 
                if (nams is not None and toks[i].name_value is not None): 
                    break
                if (typ is None): 
                    typ = toks[i]
                    ki = typ.kind
                elif (typ.kind != toks[i].kind): 
                    break
            if (toks[i].name_value is not None): 
                if (typ is not None and toks[i].kind != NamedEntityKind.UNDEFINED and toks[i].kind != typ.kind): 
                    break
                if (nams is None): 
                    nams = list()
                elif (nams[0].is_wellknown != toks[i].is_wellknown): 
                    break
                if (ki == NamedEntityKind.UNDEFINED): 
                    ki = toks[i].kind
                nams.append(toks[i])
            if (toks[i].type_value is None and toks[i].name_value is None): 
                break
            if (re is None and NamedEntityAnalyzer.__can_be_ref(ki, toks[i].ref)): 
                re = toks[i]
        else: i = len(toks)
        if ((i < len(toks)) and toks[i].ref is not None): 
            if (NamedEntityAnalyzer.__can_be_ref(ki, toks[i].ref)): 
                re = toks[i]
                i += 1
        ok = False
        if (typ is not None): 
            if (nams is None): 
                if (re is None): 
                    ok = False
                else: 
                    ok = True
            elif ((nams[0].begin_char < typ.end_char) and not nams[0].is_wellknown): 
                if (re is not None): 
                    ok = True
                elif ((nams[0].chars.is_capital_upper and not MiscHelper.can_be_start_of_sentence(nams[0].begin_token) and typ.morph.number != MorphNumber.PLURAL) and typ.morph.case.is_nominative): 
                    ok = True
            else: 
                ok = True
        elif (nams is not None): 
            if (len(nams) == 1 and nams[0].chars.is_all_lower): 
                pass
            elif (nams[0].is_wellknown): 
                ok = True
        if (not ok or ki == NamedEntityKind.UNDEFINED): 
            return None
        nam = NamedEntityReferent._new1617(ki)
        if (typ is not None): 
            nam.add_slot(NamedEntityReferent.ATTR_TYPE, typ.type_value.lower(), False, 0)
        if (nams is not None): 
            if (len(nams) == 1 and nams[0].is_wellknown and nams[0].type_value is not None): 
                nam.add_slot(NamedEntityReferent.ATTR_TYPE, nams[0].type_value.lower(), False, 0)
            if (typ is not None and (typ.end_char < nams[0].begin_char)): 
                str0_ = MiscHelper.get_text_value(nams[0].begin_token, nams[len(nams) - 1].end_token, GetTextAttr.NO)
                nam.add_slot(NamedEntityReferent.ATTR_NAME, str0_, False, 0)
            tmp = Utils.newStringIO(None)
            for n in nams: 
                if (tmp.tell() > 0): 
                    print(' ', end="", file=tmp)
                print(n.name_value, end="", file=tmp)
            nam.add_slot(NamedEntityReferent.ATTR_NAME, Utils.toStringStringIO(tmp), False, 0)
        if (re is not None): 
            nam.add_slot(NamedEntityReferent.ATTR_REF, re.ref, False, 0)
        return ReferentToken(nam, toks[0].begin_token, toks[i - 1].end_token)
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.named.internal.NamedItemToken import NamedItemToken
        from pullenti.ner.ProcessorService import ProcessorService
        try: 
            NamedItemToken._initialize()
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.register_analyzer(NamedEntityAnalyzer())