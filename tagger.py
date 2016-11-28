#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import taglib
import re
import argparse

"""

- for all files in tree: extract metadata, tag files


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
    print("----->" + tmsu_root)
    if not os.path.isdir(tmsu_root + "/.tmsu") or not os.path.exists(tmsu_root + "/.tmsu/db"):
        p = subprocess.Popen(["tmsu", "init"], cwd=tmsu_root)
        p.wait()

    if not os.path.exists(mount_point_full_path):
        os.mkdir(mount_point_full_path)


def escape_shell_chars(str):
    """
    escapes all chars which would cause problems in shell
    :param str:
    :return:
    """
    return re.sub("(!|\$|#|&|\"|\'|\(|\)|\||<|>|`|\\\|;| )", r"\\\1", str)


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
                # tag( "." + ( "{0}/{1}".format(dirName, f)[len(data_dir):] ), data_dir )
                # tag()
                #
                # try:
                #     s = taglib.File( dirName + "/" + f )
                #     #print(s.tags)
                #     for k, v in s.tags.items():
                #         print("  ", k, v)
                # except OSError as e:
                #     pass
