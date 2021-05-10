import click
import logging
import os
import pathlib
import sys
import multiprocessing 

from data_wrangler import infer_language

# Add the directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


logging.basicConfig(filename=str(pathlib.Path(__file__).parents[0].joinpath('lang_detection.log')),
                    level=logging.DEBUG)

@click.command()
@click.option('--detect_language', help='Infer language of tweets', default=False, is_flag=True)
@click.argument('data_dir', type=click.Path(exists=True)) #Path to data directory
@click.argument('tweets_file') #Name file of the tweets dataset
@click.argument('lang_file', required=False) #Name file of the given lang words
@click.option('--sample', help='Run task on a sample', default=False, is_flag=True)
@click.option('--guarani', help='Infer guarani on tweets', default=False, is_flag=True) #identify Guarani
@click.option('--lang_lookup', help='Infer given language on tweets', default=False, is_flag=True) #identify given lang
def run_task(detect_language, data_dir, tweets_file, sample, guarani, lang_file, lang_lookup):
    if detect_language:
        infer_language(data_dir, tweets_file, sample, guarani, lang_file, lang_lookup)
    else:
        click.UsageError('Illegal user: Please indicate a running option. ' \
                         'Type --help for more information of the available ' \
                         'options.')


if __name__ == '__main__':
    cd_name = os.path.basename(os.getcwd())
    if cd_name != 'src':
        click.UsageError('Illegal use: This script must run from the src directory')
    else:
        #run_task()
        cpus=int(os.cpu_count())#-1
        pool = multiprocessing.Pool(processes=cpus)
        pool.map(run_task(),)
        pool.close()
