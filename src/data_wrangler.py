import csv
import logging
import pathlib

from utils.language_detector import detect_language


logging.basicConfig(filename=str(pathlib.Path(__file__).parents[0].joinpath('tw_coronavirus.log')),
                    level=logging.DEBUG)


def infer_language(data_folder, input_file_name, sample=False):
    output_file_name = data_folder + '/tweets_languages_' + input_file_name
    input_file_name = data_folder + '/' + input_file_name
    sample_size = 100

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
    #tweet_langs = []
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
                    logging.info('[{0}] Infering language of tweet: {1}'.\
                                format(row_counter, row['tweet_id']))
                    lang, lang_fasttext, lang_langid, lang_langdetect, lang_polyglot = detect_language(row['tweet'])
                    csv_writer = csv.DictWriter(csv_out, fieldnames=['tweet_id', 'lang',
                    'lang_fasttext','lang_langid','lang_langdetect','lang_polyglot'])
                    if row_counter==1 and len(processed_tweet_ids)==0:
                        csv_writer.writeheader()
                    csv_writer.writerow({'tweet_id': row['tweet_id'], 'lang': lang,
                    'lang_fasttext': lang_fasttext, 'lang_langid': lang_langid, 'lang_langdetect': lang_langdetect,
                    'lang_polyglot': lang_polyglot})
    except Exception as e:
        logging.exception('The following error occurs when infering language '\
                          'of tweets')

    print('Process finishes successfully!')
