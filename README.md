### Partially forked from https://github.com/social-link-analytics-group-bsc/tw_coronavirus

# Installation

Install requirements `pip install -r requirements.txt`
    
Download fastText [lib](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin).

Download the crudaban corpus.

```
import nltk
nltk.download('crudaban')
```

# Command Line Interface

All commands must be run from the src directory.

## Detect language of tweets

python run.py [data_dir] [file_name_of_tweets] [language_lexicon] --detect_language --guarani

    data_dir: path to data directory and must be relative to the src directory. Required.
    file_name_of_tweets: Name of the file containing the tweets in CSV format. Required.
    language_lexicon: Name of the file containing the language's (to-identify) words lexicon. Optional. In fact, language_lexicon can be any low-resource language.
    guarani: The language (to-identify) is Guarani (or another low-resource language)? Optional. Needed for language_lexicon.
