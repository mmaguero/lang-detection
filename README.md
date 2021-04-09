### Partially forked from https://github.com/social-link-analytics-group-bsc/tw_coronavirus

# Installation

Install requirements `pip install -r requirements.txt`
    
Download fastText [lib](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin)

# Command Line Interface

All commands must be run from the src directory.

## Detect language of tweets

python run.py detect-language [data_dir] [file_name_of_tweets]

    data_dir: path to data directory and must be relative to the src directory
    file_name_of_tweets: Name of the file containing the tweets in CSV format
