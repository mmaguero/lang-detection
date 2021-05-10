import csv
import logging
import pathlib
import numpy as np

from utils.language_detector import detect_language
from utils.utility import intersecting_str, readFile


logging.basicConfig(filename=str(pathlib.Path(__file__).parents[0].joinpath('lang_detection.log')),
                    level=logging.DEBUG)


def infer_language(data_folder, input_file_name, sample=False, guarani=False, lang_file=None, lang_lookup=False):
    output_file_name = data_folder + '/tweets_languages_' + ('gn_' if lang_lookup else '') + input_file_name
    input_file_name = data_folder + '/' + input_file_name
    sample_size = 100
    y = set(readFile(lang_file)) if lang_lookup else None

    print('Starting process to infer language of tweets')

    logging.info('Looking for file that contains pre-processed tweet ids...')
    processed_tweet_ids = set()
    try:
        with open(output_file_name) as csv_file:
            logging.info('Found file with existing pre-processed tweet ids...')
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                processed_tweet_ids.add(row['tweet_id'])
    except IOError:
        pass

    logging.info('Infering language of tweets...')
    try:
        with open(input_file_name, 'r') as csv_file:
            with open(output_file_name, 'a') as csv_out:
                csv_reader = csv.DictReader(csv_file)
                row_counter = 0
                for row in csv_reader:
                    if row['tweet_id'] in processed_tweet_ids:
                        # ignore tweets that were already processed
                        continue
                    row_counter += 1
                    if sample and row_counter > sample_size:
                        break
                    if lang_lookup:
                        logging.info('[{0}] Infering -given- language of tweet: {1}'.\
                                format(row_counter, row['tweet_id']))
                        # need to improve: in only one call
                        match_contains, tokens, word_contains = intersecting_str(x=row['tweet'], y=y, method='contains')
                        match_intersection, tokens, word_intersection = intersecting_str(x=row['tweet'], y=y, method='intersection')
                        csv_writer = csv.DictWriter(csv_out, fieldnames=['tweet_id', 'tokens', 'match_contains', 'word_contains', 'match_intersection', 'word_intersection'])
                        if row_counter==1 and len(processed_tweet_ids)==0:
                            csv_writer.writeheader()
                        csv_writer.writerow({'tweet_id': row['tweet_id'], 'tokens': tokens, 'match_contains': match_contains, 'word_contains': word_contains, 'match_intersection': match_intersection, 'word_intersection': word_intersection})
                    else:
                        logging.info('[{0}] Infering language of tweet: {1}'.\
                                format(row_counter, row['tweet_id']))
                        lang, lang_fasttext, lang_langid, lang_langdetect, lang_polyglot, lang_textcat = detect_language(row['tweet'], guarani)
                        csv_writer = csv.DictWriter(csv_out, fieldnames=['tweet_id', 'lang',
                             'lang_fasttext','lang_langid','lang_langdetect','lang_polyglot', 'lang_textcat'])
                        if row_counter==1 and len(processed_tweet_ids)==0:
                            csv_writer.writeheader()
                        csv_writer.writerow({'tweet_id': row['tweet_id'], 'lang': lang,
                            'lang_fasttext': lang_fasttext, 'lang_langid': lang_langid, 'lang_langdetect': lang_langdetect,
                            'lang_polyglot': lang_polyglot, 'lang_textcat': lang_textcat})
    except Exception as e:
        logging.exception('The following error occurs when infering language '\
                          'of tweets')

    print('Process finishes successfully!')
    
