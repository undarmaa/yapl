# Word and Phrase Dictionary Extracted from Wikipedia on SQLite.

## How to use

### Download and Create Dictionary as SQLite DB.
```
$> python3 main.py
```

### Check whether a phrase exist

```
$> python3
>>> from models import WordAndPhraseDictModel
>>> wp_dict = WordAndPhraseDictModel('./wp_dict.db')
>>> wp_dict.is_phrase('ntt')
True
```

## Dataset
- [Wikimedia Downloads](https://dumps.wikimedia.org/)
