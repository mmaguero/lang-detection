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


