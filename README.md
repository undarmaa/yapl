# Word and Phrase Dictionary Extracted from Wikipedia

This script extracts word and phrase from wikipedia page titles and insterts theses data into SQLite3 database. 

## Usage
```
$ python3 main.py -h
usage: main.py [-h] [--db-path DB_PATH] [--wiki-titles-url WIKI_TITLES_URL]
               [--wiki-titles-hash WIKI_TITLES_HASH]

A Handler for Word And Phrae Dictonray.

optional arguments:
  -h, --help            show this help message and exit
  --db-path DB_PATH     sqlite3 databese path.
  --wiki-titles-url WIKI_TITLES_URL
                        wikimedia page titles url for downloading.
  --wiki-titles-hash WIKI_TITLES_HASH
                        wikimedia page titles sha256 hash for validation.
```

Default settings is here.

| arguments | default value |
|:--|:--|
| --db-path | wp_dict.db |
| --wiki-titles-url | https://dumps.wikimedia.org/enwiki/20160920/enwiki-20160920-all-titles.gz |
| --wiki-titles-hash | 9d9aea6dac7d12659f08505988db9e36920c8b58cd6468b2ccf5e0605d96de5d |

### Setup

Download and Create Dictionary as SQLite DB.
```
$ python3 main.py
```

### Basics

#### Is it phrase?
```
$ python3
>>> from models import WordAndPhraseDictModel
>>> wp_dict = WordAndPhraseDictModel('./wp_dict.db')
>>> wp_dict.is_phrase('ntt')
True
```

## Dataset
- [Wikimedia Downloads](https://dumps.wikimedia.org/)
