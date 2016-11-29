# TSMU Tagger

### Synopsis

tmsu-tagger uses music's metadata provided by taglib to tag music using [tmsu](http://tmsu.org).

### Usage
> tagger.py --data-dir=path/to/music --mountpoint-name=mp

data-dir: the directory which holds you music files
mount-point: the tmsu mountpoint in your data-dir

### Configuration
edit mappings.py to add/change the tag mappings.
This file holds a dict with keys being regexes which are matched against the tagnames of the music. Upon match, the tagvalues are used as tmsu tagvalues.

```
regexes = {
    re.compile("(?<!album)artist"): "artist", # artist but not albumartist
    re.compile("title"): "title",
    re.compile("album(?!artist)"): "album", # album but not albumartist
    re.compile("genre"): "genre",
    re.compile("((?<!tagging)(?<!rip)(?<!rip )(?<!traktorrelease))date"): "date",
    re.compile("label"): "label",
}
```

### Dependencies
- Python 3.4/3.5
- taglib

see requirements.txt

### License

MIT