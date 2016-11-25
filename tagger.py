#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import taglib
import re

"""

- for all files in tree: extract metadata, tag files


"""

data_dir = "./test_data"
mount_point_name = "mp"
full_mount_point = data_dir + "/" + mount_point_name


def init_tmsu(tmsu_root, mount_point):
    """
    initializes tmsu at tmsu_root and creates mount_point for usage as tmsu mountpoint
    :param tmsu_root: path to tmsu_root, ex. "./data"
    :param mount_point: path to mp inside tmsu_root, ex. "./data/mp"
    :return:
    """
    print("----->" + tmsu_root)
    if not os.path.isdir(tmsu_root + "/.tmsu") or not os.path.exists(tmsu_root + "/.tmsu/db"):
        p = subprocess.Popen(["tmsu", "init"], cwd=tmsu_root)
        p.wait()

    if not os.path.exists( mount_point):
        os.mkdir(mount_point)


def escape_shell_chars(str):
    """
    escapes all chars which would cause problems in shell
    :param str:
    :return:
    """
    return re.sub("(!|\$|#|&|\"|\'|\(|\)|\||<|>|`|\\\|;)", r"\\\1", str)


def tag(filename_rel_to_tmsu_root, tmsu_root):
    """

    :param filename_rel_to_tmsu_root:
    :param tmsu_root:
    :return:
    """
    print("####################")
    print(tmsu_root, filename_rel_to_tmsu_root)
    full_filename = tmsu_root + "/" +  filename_rel_to_tmsu_root
    print(full_filename)

    try:
        tl_file = taglib.File(full_filename)
        tags = []
        for tag_name, tag_value in tl_file.tags.items():
            for s in tag_value:
                tags.append( "{0}={1}".format(escape_shell_chars(tag_name.lower()), escape_shell_chars(s)))
        cmd = ["tmsu", "tag", filename_rel_to_tmsu_root] + tags
        print( cmd)
        p = subprocess.Popen(cmd, cwd=tmsu_root)
        p.wait()

    except OSError as e:
        pass


if __name__ == "__main__":
    exclude_dirs = [full_mount_point, data_dir + "/.tmsu"]
    print(exclude_dirs)

    for dirName, subDirList, fileList in os.walk(data_dir):
        print("dn", dirName)
        if dirName in exclude_dirs:
            print("skipping ", dirName)
            continue
        if len(fileList) > 0:
            for f in fileList:
                print("\t{0}/{1}".format(dirName, f))
                # try:
                #     s = taglib.File( dirName + "/" + f )
                #     #print(s.tags)
                #     for k, v in s.tags.items():
                #         print("  ", k, v)
                # except OSError as e:
                #     pass
