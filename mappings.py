#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

regexes = {
    re.compile("(?<!album)artist"): "artist", # artist but not albumartist
    re.compile("title"): "title",
    re.compile("album(?!artist)"): "album", # album but not albumartist
    re.compile("genre"): "genre",
    re.compile("((?<!tagging)(?<!rip)(?<!rip )(?<!traktorrelease))date"): "date",
    re.compile("label"): "label",
}

if __name__ == "__main__":
    print("this file contains the mapping info for the tagger.")