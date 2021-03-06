#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import taglib
import argparse
import re

import mappings

"""
tmsu problems:
- tmsu unmount does not work on ubuntu 14.04
- when traversing mountpoint with os.walk(...) and aborting with ^C tmsu crashes(?) and mountpoint becomes unuseable
"""

data_dir = "./test_data"
default_mount_point_name = "mp"
full_mount_point = data_dir + "/" + default_mount_point_name

def init_tmsu(tmsu_root, mount_point_full_path):
    """
    initializes tmsu at tmsu_root and creates mount_point for usage as tmsu mountpoint
    :param tmsu_root: path to tmsu_root, ex. "./data"
    :param mount_point_full_path: path to mp inside tmsu_root, ex. "./data/mp"
    :return:
    """

    if not os.path.isdir(tmsu_root + "/.tmsu") or not os.path.exists(tmsu_root + "/.tmsu/db"):
        p = subprocess.Popen(["tmsu", "init"], cwd=tmsu_root)
        p.wait()

    if not os.path.exists(mount_point_full_path):
        os.mkdir(mount_point_full_path)


def escape_shell_chars_tmsu(str):
    """
    escapes all chars which would cause problems in shell and
    also replaces / with \, because tmsu does not accept \ in tags
    :param str:
    :return:
    """
    str = str.replace("/", "\\")
    str = re.sub("(!|\$|#|&|\"|\'|\(|\)|\||<|>|`|\\\|;| )", r"\\\1", str)
    return str


def get_filtered_taglist(taglib_tags):
    res = []
    for tag_name, tag_values in taglib_tags.items():
        for r, mapped_name in mappings.regexes.items():
            r_matches = r.findall( tag_name.lower() )
            if len(r_matches) > 0:
                res += [mapped_name + "=" + escape_shell_chars_tmsu(v) for v in tag_values]
    return res


def tag(filename_rel_to_tmsu_root, tmsu_root):
    """

    :param filename_rel_to_tmsu_root:
    :param tmsu_root:
    :return:
    """
    full_filename = tmsu_root + "/" +  filename_rel_to_tmsu_root

    try:
        tl_file = taglib.File(full_filename)
        tag_str = get_filtered_taglist(tl_file.tags)
        cmd = ["tmsu", "tag", filename_rel_to_tmsu_root ] + tag_str
        p = subprocess.Popen(cmd, cwd=tmsu_root)
        p.wait()

    except OSError as e:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser("tagger")
    parser.add_argument("--data-dir",        "-d",                 nargs=1, type=str, required=True,  help="the dir holding the data")
    parser.add_argument("--mountpoint-name", "-m", default=["mp"], nargs=1, type=str, required=False, help="optional mountpointname if different than 'mp'")

    args = parser.parse_args()

    data_dir = args.data_dir[0]
    mountpoint_name = args.mountpoint_name[0]

    exclude_dirs = [mountpoint_name, ".tmsu"]

    init_tmsu( data_dir, data_dir + "/" + mountpoint_name )

    for dirName, subDirList, fileList in os.walk(data_dir, topdown=True):
        #remove exclude_dirs
        subDirList[:] = [ d for d in subDirList if d not in exclude_dirs ]
        print("processing", dirName)
        for f in fileList:
            tag( "." + ( "{0}/{1}".format(dirName, f)[len(data_dir):] ), data_dir )
