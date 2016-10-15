# YAPL - Yet Another Phrase Lexicon
Word and Phrase Lexicon Extracted from Wikipedia to SQLite3.

## Usage
```
$ python3 yapl.py -h
usage: yapl.py [-h] [--db-path DB_PATH] [--wiki-titles-url WIKI_TITLES_URL]
               [--wiki-titles-hash WIKI_TITLES_HASH]
               [--wiki-articles-url WIKI_ARTICLES_URL]
               [--wiki-articles-hash WIKI_ARTICLES_HASH]
               [--wiki-extracted-dir WIKI_EXTRACTED_DIR]

A Script for Create Phrae Lexicon Databse

optional arguments:
  -h, --help            show this help message and exit
  --db-path DB_PATH     sqlite3 databese path.
  --wiki-titles-url WIKI_TITLES_URL
                        wikimedia page titles url for downloading.
  --wiki-titles-hash WIKI_TITLES_HASH
                        wikimedia page titles sha1 hash for validation.
  --wiki-articles-url WIKI_ARTICLES_URL
                        wikimedia pages articles url for downloading.
  --wiki-articles-hash WIKI_ARTICLES_HASH
                        wikimedia page articles sha1 hash for validation.
  --wiki-extracted-dir WIKI_EXTRACTED_DIR
                        directory path of extracted xml using wikiextractor
```

### Install

Download and Create Dictionary as SQLite DB.

```
$ ./install.sh
```

### Basics

#### Is it phrase?
```
$ python3
>>> from yapl.models import WordAndPhraseDictModel
>>> lexicon = PhraseLexiconModel('yapl.db')
>>> lexicon.is_phrase('ntt')
True
```

## Dataset
This project uses [wikimedia](https://dumps.wikimedia.org/) dataset for test.  
these data under the GFDL and the [Creative Commons Attribution-Share-Alike 3.0 License](https://creativecommons.org/licenses/by-sa/3.0/).

