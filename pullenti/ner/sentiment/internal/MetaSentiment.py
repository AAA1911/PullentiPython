﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ntopy.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.sentiment.SentimentKind import SentimentKind


class MetaSentiment(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.sentiment.SentimentReferent import SentimentReferent
        super().__init__()
        f = self.add_feature(SentimentReferent.ATTR_KIND, "Тип", 1, 1)
        MetaSentiment.FTYP = f
        f.add_value(Utils.enumToString(SentimentKind.UNDEFINED), "Неизвестно", None, None)
        f.add_value(Utils.enumToString(SentimentKind.POSITIVE), "Положительно", None, None)
        f.add_value(Utils.enumToString(SentimentKind.NEGATIVE), "Отрицательно", None, None)
        self.add_feature(SentimentReferent.ATTR_SPELLING, "Текст", 0, 0)
        self.add_feature(SentimentReferent.ATTR_REF, "Ссылка", 0, 0)
        self.add_feature(SentimentReferent.ATTR_COEF, "Коэффициент", 0, 0)
    
    FTYP = None
    
    @property
    def name(self) -> str:
        from pullenti.ner.sentiment.SentimentReferent import SentimentReferent
        return SentimentReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Сентимент"
    
    IMAGE_ID_GOOD = "good"
    
    IMAGE_ID_BAD = "bad"
    
    IMAGE_ID = "unknown"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.sentiment.SentimentReferent import SentimentReferent
        sy = (obj if isinstance(obj, SentimentReferent) else None)
        if (sy is not None): 
            if (sy.kind == SentimentKind.POSITIVE): 
                return MetaSentiment.IMAGE_ID_GOOD
            if (sy.kind == SentimentKind.NEGATIVE): 
                return MetaSentiment.IMAGE_ID_BAD
        return MetaSentiment.IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaSentiment
    @staticmethod
    def _static_ctor():
        MetaSentiment._global_meta = MetaSentiment()

MetaSentiment._static_ctor()