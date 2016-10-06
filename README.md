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

Default settings is here.

| arguments | default value |
|:--|:--|
| --db-path | yapl.db |
| --wiki-titles-url | https://dumps.wikimedia.org/enwiki/20160920/enwiki-20160920-all-titles.gz |
| --wiki-titles-hash | 12c769accf4dbbe928562035fb8f3f45acf0e935 |
| --wiki-articles-url | https://dumps.wikimedia.org/enwiki/20160920/enwiki-20160920-pages-articles.xml.bz2 |
| --wiki-articles-hash | ffd929d8e3a1a48ced4785cc7726a6eaca8e3a6b' |
| --wiki-articles-text | |

### Setup

Download and Create Dictionary as SQLite DB.

```
$ python3 yapl.py
```

### Basics

#### Is it phrase?
```
$ python3
>>> from models import WordAndPhraseDictModel
>>> lexicon = PhraseLexiconModel('yapl.db')
>>> lexicon.is_phrase('ntt')
True
```

## Dataset
- [Wikimedia Downloads](https://dumps.wikimedia.org/)
