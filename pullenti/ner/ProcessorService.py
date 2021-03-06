﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import datetime
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.ImageWrapper import ImageWrapper
from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.morph.Morphology import Morphology
from pullenti.morph.Explanatory import Explanatory
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.NumberHelper import NumberHelper

class ProcessorService:
    """ Глобальная служба семантического процессора """
    
    @staticmethod
    def get_version() -> str:
        """ Версия системы """
        return "3.20.2"
    
    @staticmethod
    def get_version_date() -> datetime.datetime:
        """ Дата-время текущей версии """
        return datetime.datetime(2019, 11, 9, 0, 0, 0)
    
    @staticmethod
    def initialize(lang : 'MorphLang'=None) -> None:
        """ Инициализация сервиса.  
         Внимание! После этого нужно инициализровать анализаторы (см. документацию)
         <param name="lang">необходимые языки (по умолчанию, русский и английский)</param> """
        from pullenti.ner.core.internal.NumberExHelper import NumberExHelper
        from pullenti.ner.core.internal.BlockLine import BlockLine
        from pullenti.ner.core.internal.NounPhraseItem import NounPhraseItem
        from pullenti.ner.core.PrepositionHelper import PrepositionHelper
        from pullenti.ner.core.ConjunctionHelper import ConjunctionHelper
        if (ProcessorService.__m_inited): 
            return
        ProcessorService.__m_inited = True
        Morphology.initialize(lang)
        Explanatory.initialize(lang)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
        PrepositionHelper._initialize()
        ConjunctionHelper._initialize()
        NounPhraseItem._initialize()
        NumberHelper._initialize()
        NumberExHelper._initialize()
        BlockLine.initialize()
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
    
    __m_inited = None
    
    @staticmethod
    def is_initialized() -> bool:
        """ Признак того, что инициализация сервиса уже была """
        return ProcessorService.__m_inited
    
    @staticmethod
    def create_processor() -> 'Processor':
        """ Создать процессор со стандартным списком анализаторов (у которых свойство IsSpecific = false)
        
        Returns:
            Processor: экземпляр процессора
        """
        from pullenti.ner.Processor import Processor
        if (not ProcessorService.__m_inited): 
            return None
        proc = Processor()
        for t in ProcessorService.__m_analizer_instances: 
            a = t.clone()
            if (a is not None and not a.is_specific): 
                proc.add_analyzer(a)
        return proc
    
    @staticmethod
    def create_specific_processor(spec_analyzer_names : str) -> 'Processor':
        """ Создать процессор с набором стандартных и указанных параметром специфических
         анализаторов.
        
        Args:
            spec_analyzer_names(str): можно несколько, разделённые запятой или точкой с запятой. 
         Если список пустой, то эквивалентно CreateProcessor()
        
        """
        from pullenti.ner.Processor import Processor
        if (not ProcessorService.__m_inited): 
            return None
        proc = Processor()
        names = list(Utils.splitString((Utils.ifNotNull(spec_analyzer_names, "")), ',' + ';' + ' ', False))
        for t in ProcessorService.__m_analizer_instances: 
            a = t.clone()
            if (a is not None): 
                if (not a.is_specific or a.name in names): 
                    proc.add_analyzer(a)
        return proc
    
    @staticmethod
    def create_empty_processor() -> 'Processor':
        """ Создать экземпляр процессора с пустым списком анализаторов
        
        """
        from pullenti.ner.Processor import Processor
        return Processor()
    
    @staticmethod
    def register_analyzer(analyzer : 'Analyzer') -> None:
        """ Регистрация аналозатора. Вызывается при инициализации из инициализируемой сборки
         (она сама знает, какие содержит анализаторы, и регистрирует их)
        
        Args:
            analyzer(Analyzer): 
        """
        try: 
            ProcessorService.__m_analizer_instances.append(analyzer)
            img = analyzer.images
            if (img is not None): 
                for kp in img.items(): 
                    if (not kp[0] in ProcessorService.__m_images): 
                        ProcessorService.__m_images[kp[0]] = ImageWrapper._new2855(kp[0], kp[1])
        except Exception as ex: 
            pass
        ProcessorService.__reorder_cartridges()
    
    __m_analizer_instances = None
    
    @staticmethod
    def __reorder_cartridges() -> None:
        if (len(ProcessorService.__m_analizer_instances) == 0): 
            return
        k = 0
        while k < len(ProcessorService.__m_analizer_instances): 
            i = 0
            first_pass3352 = True
            while True:
                if first_pass3352: first_pass3352 = False
                else: i += 1
                if (not (i < (len(ProcessorService.__m_analizer_instances) - 1))): break
                max_ind = -1
                li = ProcessorService.__m_analizer_instances[i].used_extern_object_types
                if (li is not None): 
                    for v in ProcessorService.__m_analizer_instances[i].used_extern_object_types: 
                        j = i + 1
                        while j < len(ProcessorService.__m_analizer_instances): 
                            if (ProcessorService.__m_analizer_instances[j].type_system is not None): 
                                for st in ProcessorService.__m_analizer_instances[j].type_system: 
                                    if (st.name == v): 
                                        if ((max_ind < 0) or (max_ind < j)): 
                                            max_ind = j
                                        break
                            j += 1
                if (max_ind <= i): 
                    if (ProcessorService.__m_analizer_instances[i].is_specific and not ProcessorService.__m_analizer_instances[i + 1].is_specific): 
                        pass
                    else: 
                        continue
                cart = ProcessorService.__m_analizer_instances[i]
                del ProcessorService.__m_analizer_instances[i]
                ProcessorService.__m_analizer_instances.append(cart)
            k += 1
    
    @staticmethod
    def get_analyzers() -> typing.List['Analyzer']:
        """ Экземпляры доступных анализаторов """
        return ProcessorService.__m_analizer_instances
    
    @staticmethod
    def create_referent(type_name : str) -> 'Referent':
        """ Создать экземпляр объекта заданного типа
        
        Args:
            type_name(str): имя типа
        
        Returns:
            Referent: результат
        """
        from pullenti.ner.Referent import Referent
        for cart in ProcessorService.__m_analizer_instances: 
            obj = cart.create_referent(type_name)
            if (obj is not None): 
                return obj
        return Referent(type_name)
    
    __m_images = None
    
    __m_unknown_image = None
    
    @staticmethod
    def get_image_by_id(image_id : str) -> 'ImageWrapper':
        """ Получить иконку по идентификатору иконки
        
        Args:
            image_id(str): 
        
        """
        if (image_id is not None): 
            wrapres2856 = RefOutArgWrapper(None)
            inoutres2857 = Utils.tryGetValue(ProcessorService.__m_images, image_id, wrapres2856)
            res = wrapres2856.value
            if (inoutres2857): 
                return res
        if (ProcessorService.__m_unknown_image is None): 
            ProcessorService.__m_unknown_image = ImageWrapper._new2855("unknown", EpNerCoreInternalResourceHelper.get_bytes("unknown.png"))
        return ProcessorService.__m_unknown_image
    
    @staticmethod
    def add_image(image_id : str, content : bytearray) -> None:
        """ Добавить специфическую иконку
        
        Args:
            image_id(str): идентификатор (возвращаемый Referent.getImageId())
            content(bytearray): содержимое иконки
        """
        if (image_id is None): 
            return
        wr = ImageWrapper._new2855(image_id, content)
        if (image_id in ProcessorService.__m_images): 
            ProcessorService.__m_images[image_id] = wr
        else: 
            ProcessorService.__m_images[image_id] = wr
    
    __m_empty_processor = None
    
    @staticmethod
    def get_empty_processor() -> 'Processor':
        """ Экземпляр процессора с пустым множеством анализаторов (используется для
         разных лингвистических процедур, где не нужны сущности) """
        if (ProcessorService.__m_empty_processor is None): 
            ProcessorService.__m_empty_processor = ProcessorService.create_empty_processor()
        return ProcessorService.__m_empty_processor
    
    # static constructor for class ProcessorService
    @staticmethod
    def _static_ctor():
        ProcessorService.__m_analizer_instances = list()
        ProcessorService.__m_images = dict()

ProcessorService._static_ctor()