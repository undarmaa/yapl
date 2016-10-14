# YAPL - Yet Another Phrase Lexicon
Word and Phrase Lexicon Extracted from Wikipedia to SQLite3.

## Usage
```
$ python3 yapl.py -h
usage: yapl.py [-h] [--db-path DB_PATH] [--wiki-titles-url WIKI_TITLES_URL]
               [--wiki-titles-hash WIKI_TITLES_HASH]

A Handler for Word And Phrae Dictonray.

optional arguments:
  -h, --help            show this help message and exit
  --db-path DB_PATH     sqlite3 databese path.
  --wiki-titles-url WIKI_TITLES_URL
                        wikimedia page titles url for downloading.
  --wiki-titles-hash WIKI_TITLES_HASH
                        wikimedia page titles sha1 hash for validation.
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
- [Wikimedia Downloads](https://dumps.wikimedia.org/)
