#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import taglib

"""

- check if tmsu init was called - if .tmsu folder exists
- tmsu init if needed
- for all files in tree: extract metadata, tag files


"""

data_dir = "./test_data"


def init_tmsu(tmsu_dir):
    if not os.path.isdir(tmsu_dir + "/.tmsu") or not os.path.exists(tmsu_dir + "/.tmsu/db"):
        p = subprocess.Popen(["tmsu", "init"], cwd=tmsu_dir)
        p.wait()



if __name__ == "__main__":
    print("hello world")

    for dirName, subDirList, fileList in os.walk(data_dir):
        if len(fileList) > 0:
            for f in fileList:
                print("{0}/{1}".format(dirName, f))
                try:
                    s = taglib.File( dirName + "/" + f )
                    #print(s.tags)
                    for k, v in s.tags.items():
                        print("  ", k, v)
                except OSError as e:
                    pass
