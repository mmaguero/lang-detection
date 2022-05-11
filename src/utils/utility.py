#utils.py

import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import RegexpTokenizer


def intersecting_str(x,y,method='contains'):
  '''
   Set (per Guarani) with the top M most frequent words or dictionary. Then intersect|contains your text with each set. The set with the highest number of intersections|coincides will be your detected language: Guarani.
   x = text convert to set ... of words to infer language (i.e, tweets)
   y = file convert to set ... of words of the language to infer (i.e., Guarani dictionary)
   method = intersection|contains
   return = tuple() of number of x in y words, and number of x words, also the match words are given
   finally = with the tuple... percent: divide the number of words by the total number of words in the text, or
                               count:   take those with more than X words in the dictionary
  '''
  # convert x (text) to set 
  tokenizer = RegexpTokenizer(r"(\w+\'\w?)|(\w+)") # alphabetic characters only + '...
  words = tokenizer.tokenize(str(x)) # return tuples because "|" #word_tokenize(str(x)) #set(str(x).lower().split()) 
  x = set([t[0] for t in words]+[t[1] for t in words])
  # convert y (file) to set
  #y = set(readFile(y))
  #
  if method=='contains':
    # prepare set
    try:
      xnp = np.array(x)
      xpd = pd.DataFrame(x)
      xpd.columns=["col"]
      gn=xpd[xpd.col.str.contains('|'.join(y))].reset_index() # partial match: e.g., "omba'apo" contains "apo" = TRUE
      gn=gn.col.tolist()
    except:
      gn=list()
  elif method=='intersection':
    gn = x.intersection(y) # strict match: e.g., "omba'apo" intersect "apo" = FALSE

  match = set(list(gn))
  return len(gn), len(x), match


def readFile(fileName):
    fileObj = open(fileName, "r") #opens the file in read mode
    words = [line.split(",") for line in fileObj.read().splitlines()] # puts the file into an array
    merged_list = []
    for l in words: # an array from the list of arrays:  syn/n-grams comma separated support
      merged_list += l
    fileObj.close()
    return [word for word in merged_list if len(word)>2]


ISO_639_1_TO_3 = {
    'aa': 'aar',
    'ab': 'abk',
    'ae': 'ave',
    'af': 'afr',
    'ak': 'aka',
    'am': 'amh',
    'an': 'arg',
    'ar': 'ara',
    'as': 'asm',
    'av': 'ava',
    'ay': 'aym',
    'az': 'aze',
    'ba': 'bak',
    'be': 'bel',
    'bg': 'bul',
    'bi': 'bis',
    'bm': 'bam',
    'bn': 'ben',
    'bo': 'bod',
    'br': 'bre',
    'bs': 'bos',
    'ca': 'cat',
    'ce': 'che',
    'ch': 'cha',
    'co': 'cos',
    'cr': 'cre',
    'cs': 'ces',
    'cu': 'chu',
    'cv': 'chv',
    'cy': 'cym',
    'da': 'dan',
    'de': 'deu',
    'dv': 'div',
    'dz': 'dzo',
    'ee': 'ewe',
    'el': 'ell',
    'en': 'eng',
    'eo': 'epo',
    'es': 'spa',
    'et': 'est',
    'eu': 'eus',
    'fa': 'fas',
    'ff': 'ful',
    'fi': 'fin',
    'fj': 'fij',
    'fo': 'fao',
    'fr': 'fra',
    'fy': 'fry',
    'ga': 'gle',
    'gd': 'gla',
    'gl': 'glg',
    'gn': 'grn',
    'gu': 'guj',
    'gv': 'glv',
    'ha': 'hau',
    'he': 'heb',
    'hi': 'hin',
    'ho': 'hmo',
    'hr': 'hrv',
    'ht': 'hat',
    'hu': 'hun',
    'hy': 'hye',
    'hz': 'her',
    'ia': 'ina',
    'id': 'ind',
    'ie': 'ile',
    'ig': 'ibo',
    'ii': 'iii',
    'ik': 'ipk',
    'io': 'ido',
    'is': 'isl',
    'it': 'ita',
    'iu': 'iku',
    'ja': 'jpn',
    'jv': 'jav',
    'ka': 'kat',
    'kg': 'kon',
    'ki': 'kik',
    'kj': 'kua',
    'kk': 'kaz',
    'kl': 'kal',
    'km': 'khm',
    'kn': 'kan',
    'ko': 'kor',
    'kr': 'kau',
    'ks': 'kas',
    'ku': 'kur',
    'kv': 'kom',
    'kw': 'cor',
    'ky': 'kir',
    'la': 'lat',
    'lb': 'ltz',
    'lg': 'lug',
    'li': 'lim',
    'ln': 'lin',
    'lo': 'lao',
    'lt': 'lit',
    'lu': 'lub',
    'lv': 'lav',
    'mg': 'mlg',
    'mh': 'mah',
    'mi': 'mri',
    'mk': 'mkd',
    'ml': 'mal',
    'mn': 'mon',
    'mr': 'mar',
    'ms': 'msa',
    'mt': 'mlt',
    'my': 'mya',
    'na': 'nau',
    'nb': 'nob',
    'nd': 'nde',
    'ne': 'nep',
    'ng': 'ndo',
    'nl': 'nld',
    'nn': 'nno',
    'no': 'nor',
    'nr': 'nbl',
    'nv': 'nav',
    'ny': 'nya',
    'oc': 'oci',
    'oj': 'oji',
    'om': 'orm',
    'or': 'ori',
    'os': 'oss',
    'pa': 'pan',
    'pi': 'pli',
    'pl': 'pol',
    'ps': 'pus',
    'pt': 'por',
    'qu': 'que',
    'rm': 'roh',
    'rn': 'run',
    'ro': 'ron',
    'ru': 'rus',
    'rw': 'kin',
    'sa': 'san',
    'sc': 'srd',
    'sd': 'snd',
    'se': 'sme',
    'sg': 'sag',
    'sh': 'hbs',
    'si': 'sin',
    'sk': 'slk',
    'sl': 'slv',
    'sm': 'smo',
    'sn': 'sna',
    'so': 'som',
    'sq': 'sqi',
    'sr': 'srp',
    'ss': 'ssw',
    'st': 'sot',
    'su': 'sun',
    'sv': 'swe',
    'sw': 'swa',
    'ta': 'tam',
    'te': 'tel',
    'tg': 'tgk',
    'th': 'tha',
    'ti': 'tir',
    'tk': 'tuk',
    'tl': 'tgl',
    'tn': 'tsn',
    'to': 'ton',
    'tr': 'tur',
    'ts': 'tso',
    'tt': 'tat',
    'tw': 'twi',
    'ty': 'tah',
    'ug': 'uig',
    'uk': 'ukr',
    'ur': 'urd',
    'uz': 'uzb',
    've': 'ven',
    'vi': 'vie',
    'vo': 'vol',
    'wa': 'wln',
    'wo': 'wol',
    'xh': 'xho',
    'yi': 'yid',
    'yo': 'yor',
    'za': 'zha',
    'zh': 'zho',
    'zu': 'zul'}
    
def set_iso_639(code, source=3, target=1):
    try:
        if source == 3:
            # 639-3 to 1 
            # first, invert dict
            ISO_639_3_TO_1 = {v: k for k, v in ISO_639_1_TO_3.items()}
            #
            return ISO_639_3_TO_1[code]
        elif source == 1:
            # 639-1 to 3
            return ISO_639_1_TO_3[code]
    except:
        return 'undefined'
