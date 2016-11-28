#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import taglib
import re
import argparse
import re

"""

- for all files in tree: extract metadata, tag files


tmsu problems:
- tmsu unmount does not work on ubuntu 14.04
- when traversing mountpoint with os.walk(...) and aborting with ^C tmsu crashes(?) and mountpoint becomes unuseable

"""

data_dir = "./test_data"
default_mount_point_name = "mp"
full_mount_point = data_dir + "/" + default_mount_point_name

regexes = {
    re.compile("(?<!album)artist"): "artist", # artist but not albumartist
    re.compile("title"): "title",
    re.compile("album(?!artist)"): "album", # album but not albumartist
    re.compile("genre"): "genre",
    re.compile("((?<!tagging)(?<!rip)(?<!rip )(?<!traktorrelease))date"): "date",
    re.compile("label"): "label",
}

def init_tmsu(tmsu_root, mount_point_full_path):
    """
    initializes tmsu at tmsu_root and creates mount_point for usage as tmsu mountpoint
    :param tmsu_root: path to tmsu_root, ex. "./data"
    :param mount_point_full_path: path to mp inside tmsu_root, ex. "./data/mp"
    :return:
    """
    print("----->" + tmsu_root)
    if not os.path.isdir(tmsu_root + "/.tmsu") or not os.path.exists(tmsu_root + "/.tmsu/db"):
        p = subprocess.Popen(["tmsu", "init"], cwd=tmsu_root)
        p.wait()

    print(mount_point_full_path)
    if not os.path.exists(mount_point_full_path):
        print("tralala")
        os.mkdir(mount_point_full_path)


def escape_shell_chars(str):
    """
    escapes all chars which would cause problems in shell
    :param str:
    :return:
    """
    return re.sub("(!|\$|#|&|\"|\'|\(|\)|\||<|>|`|\\\|;| )", r"\\\1", str)


def get_filtered_taglist(taglib_tags):
    res = []
    for tag_name, tag_values in taglib_tags.items():
        for r, mapped_name in regexes.items():
            r_matches = r.findall( tag_name.lower() )
            if len(r_matches) > 0:
                res += [ mapped_name + "=" + escape_shell_chars(v) for v in tag_values ]
    return res


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

        tag_str = get_filtered_taglist(tl_file.tags)
        print("tags", tl_file.tags)
        print("tag_str:", tag_str)

        cmd = ["tmsu", "tag", filename_rel_to_tmsu_root ] + tag_str
        p = subprocess.Popen(cmd, cwd=tmsu_root)
        p.wait()

    except OSError as e:
        pass


if __name__ == "__main__":
    """
    needed args:
    - data_dir
    - opt:
    -- mount_point
    """

    parser = argparse.ArgumentParser("tagger")
    parser.add_argument("--data-dir",        "-d",                 nargs=1, type=str, required=True,  help="the dir holding the data")
    parser.add_argument("--mountpoint-name", "-m", default=["mp"], nargs=1, type=str, required=False, help="optional mountpointname if different than 'mp'")

    args = parser.parse_args()

    print("args", args)

    print(args.data_dir)
    data_dir = args.data_dir[0]
    mountpoint_name = args.mountpoint_name[0]

    exclude_dirs = [mountpoint_name, ".tmsu"]
    print("exclude_dirs", exclude_dirs)

    init_tmsu( data_dir, data_dir + "/" + mountpoint_name )

    for dirName, subDirList, fileList in os.walk(data_dir, topdown=True):
        #remove exclude_dirs
        subDirList[:] = [ d for d in subDirList if d not in exclude_dirs ]

        print("dn", dirName)

        if len(fileList) > 0:
            for f in fileList:
                print("\t{0}/{1}".format(dirName, f))

                print("\t\t", "." + ( "{0}/{1}".format(dirName, f)[len(data_dir):] ))
                tag( "." + ( "{0}/{1}".format(dirName, f)[len(data_dir):] ), data_dir )
