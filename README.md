# Detectors

Tools used for this purpose: 
- [polyglot](https://github.com/aboSamoor/polyglot)*, 
- [fastText](https://github.com/facebookresearch/fastText/tree/master/python)*, 
- [langdetect](https://pypi.org/project/langdetect/),
- [langid](https://github.com/saffsd/langid.py), and
- [textcat](https://www.nltk.org/_modules/nltk/classify/textcat.html)*.

\*: Supports the Guarani language.

# Installation

## Pre-requisites:

Install [**polyglot** dependencies](https://github.com/aboSamoor/polyglot/blob/master/docs/Installation.rst).

Install requirements `pip install -r requirements.txt`
    
Download fastText [lib](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin).

Download the crubadan corpus.

```
import nltk
nltk.download('crubadan')
nltk.download('punkt')
```

# Command Line Interface

All commands must be run from the src directory.

## Detect language of tweets

`python run.py [data_dir] [file_name_of_tweets] [language_lexicon] --detect_language --guarani`

    data_dir: path to data directory and must be relative to the src directory. Required.
    file_name_of_tweets: Name of the file containing the tweets in CSV format. Required.
    language_lexicon: Name of the file containing the language's (to-identify) words lexicon. Optional. In fact, language_lexicon can be any low-resource language.
    guarani: The language (to-identify) is Guarani (or another low-resource language)? Optional. Needed for language_lexicon.
    
See also: [lang](lang.cmd), [lang_2](lang_2.cmd).

---
Note: <small>Partially forked from https://github.com/social-link-analytics-group-bsc/tw_coronavirus in v1.0.</small>
