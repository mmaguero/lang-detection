import os

from collections import defaultdict
import numpy as np
import math

# Language detection tools
import fasttext
from langdetect import detect_langs
from polyglot.detect import Detector
from langid.langid import LanguageIdentifier, model
from nltk.classify import textcat
from utility import set_iso_639


# Load module for fasttext
ft_model = fasttext.load_model('lib/lid.176.bin')

# Instiantiate a langid language identifier object
langid_identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

# Instiantiate a textcat language classifier
tc_cls = textcat.TextCat()


def detect_language(text, guarani=False):
    '''
    return ISO 639-1
    '''
    threshold_confidence = 0.70 # changed because gn,grn,gug is tricky, old 0.75
    lang_detected = defaultdict(int)

    if not text:
        raise Exception('Error!, text is empty.')

    # infer language using fasttext
    try:
        pred_fasttext = ft_model.predict(text, k=1)
        if pred_fasttext[1][0] >= threshold_confidence:
            lang_fasttext = pred_fasttext[0][0].replace('__label__','')
        else:
            lang_fasttext = 'undefined'
    except:
        lang_fasttext = 'undefined'
    lang_detected[lang_fasttext] += 1

    # infer language using langid
    try:
        pred_langid = langid_identifier.classify(text) if not guarani else None # raise exception, gn not supported
        if pred_langid[1] >= threshold_confidence:
            lang_langid = pred_langid[0]
        else:
            lang_langid = 'undefined'
    except:
        lang_langid = 'undefined' if not guarani else None # raise exception, gn not supported
    lang_detected[lang_langid] += 1

    # infer language using langdetect
    try:
        pred_langdetect = detect_langs(text)[0] if not guarani else None # raise exception, gn not supported
        lang_langdetect, conf_langdetect = str(pred_langdetect).split(':')
        conf_langdetect = float(conf_langdetect)
        if conf_langdetect < threshold_confidence:
            lang_langdetect = 'undefined'
    except:
        lang_langdetect = 'undefined' if not guarani else None # raise exception, gn not supported
    lang_detected[lang_langdetect] += 1

    # infer language using polyglot
    try:
        poly_detector = Detector(text, quiet=True)
        lang_polyglot = poly_detector.language.code
        conf_polyglot = poly_detector.language.confidence/100
        if conf_polyglot >= threshold_confidence:
            # sometimes polyglot  returns the language
            # code with an underscore, e.g., zh_Hant.
            # next, the underscore is removed
            idx_underscore = lang_polyglot.find('_')
            if idx_underscore != -1:
                lang_polyglot = lang_polyglot[:idx_underscore]
        else:
            lang_polyglot = 'undefined'
    except:
        lang_polyglot = 'undefined'
    lang_detected[lang_polyglot] += 1
    
    # infer language using textcat
    # WARN: unlike the others, this one returns ISO 639-3
    try:
        # distances
        distances = tc_cls.lang_dists(text)  # a dict of 437 elements
        lang_textcat_far = max(distances.values())
        lang_textcat_near = min(distances.values()) # lang identified
        #softmax for normalization 0-1 for confidence
        numbers=[math.log(lang_textcat_near),math.log(lang_textcat_far)] # apply log for avoid skewness, floating-point precision problems
        exponentials = np.exp(numbers)
        sum_exponentials = np.sum(exponentials)
        softmax = exponentials/sum_exponentials
        # and ..
        conf_textcat = float(abs(softmax[0]-1)) # get softmax of min distance, substract 1 for inverse value
        lang_textcat = tc_cls.guess_language(text)  # a str with min distance (near to lang)
        # to ISO 639-1
        lang_textcat = set_iso_639(lang_textcat)
        if conf_textcat < threshold_confidence:
            lang_textcat = 'undefined'
    except Exception as e:
        lang_textcat = 'undefined'
        print('lang_textcat',e)
    lang_detected[lang_textcat] += 1

    # choose language with the highest counter
    max_counter, pref_lang = -1, ''
    for lang, counter in lang_detected.items():
        if lang == 'undefined' or not lang:
            continue
        if counter > max_counter:
            pref_lang = lang
            max_counter = counter
        elif counter == max_counter:
            pref_lang += '_' + lang

    return (pref_lang if pref_lang != '' else 'undefined', lang_fasttext, lang_langid, lang_langdetect, lang_polyglot, lang_textcat)
    
