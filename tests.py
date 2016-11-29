#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import shutil
import subprocess
import re

import tagger

data_dir = "./test_data"

tmsu_dir = data_dir + "/.tmsu"
mount_point = "mp"
mount_point_full_path = data_dir + "/" + mount_point

music_file = "Bibi Blocksberg - Hex Hex (Remix).ogg"


class TestTMSUInit(unittest.TestCase):
    def setUp(self):
        self.tmsu_dir = data_dir + "/.tmsu"
        self._remove_tmsu()

    def tearDown(self):
        self._remove_tmsu()
        shutil.rmtree(mount_point_full_path)
        pass

    @staticmethod
    def _remove_tmsu():
        if os.path.exists(tmsu_dir):
            shutil.rmtree(tmsu_dir)

    def test_init(self):
        tagger.init_tmsu(data_dir, mount_point_full_path)

        self.assertTrue(os.path.isdir(tmsu_dir))
        self.assertTrue(os.path.exists(tmsu_dir+"/db"))
        self.assertTrue(os.path.isdir(mount_point_full_path))


# class TestTagMatching(unittest.TestCase):
#     def setUp(self):
#         self.regexes = {
#             re.compile("artist") : "artist",
#             re.compile("title") :  "title",
#             re.compile("album") :  "album",
#             re.compile("genre") :  "genre",
#             re.compile("((?<!tagging)(?<!rip)(?<!rip )(?<!traktorrelease))date"): "date",
#             re.compile("label") :  "label",
#         }
#         pass
#
#     def tearDown(self):
#         pass
#
#     def test_matching(self):



# class TestTagging(unittest.TestCase):
#     def setUp(self):
#         print("2222222222")
#         tagger.init_tmsu(data_dir, mount_point_full_path)
#         self.mount()
#
#     def tearDown(self):
#         self.unmount()
#         # dont remove, because it's mounted
#         # TestTMSUInit._remove_tmsu()
#
#     @staticmethod
#     def mount():
#         print("MOUNTING")
#         p = subprocess.Popen(["tmsu", "mount", mount_point ], cwd=data_dir)
#         p.wait()
#         pass
#
#     @staticmethod
#     def unmount():
#         # wait until tmsu can unmount on it's own on ubuntu 14.04
#         pass
#
#     def test_tagging(self):
#         check_values = {
#             'artist': ['Bibi Blocksberg'],
#             'compilation': ['0'],
#             'date': ['-1'],
#             'title': ['Hex Hex (Remix)'],
#             'tracknumber': ['-1']
#         }
#
#         tagger.tag(music_file, data_dir)
#
#         print(mount_point_full_path, "/tags")
#
#         for dir_name, subdir_list, file_list in os.walk(mount_point_full_path + "/tags"):
#             print(dir_name)
#             for f in file_list:
#                 print("\t", f)
#                 self.assertTrue( f in check_values.keys() )






if __name__ == "__main__":
    print("AAAAAAAARRRRRRRRRGGGGGGGGGHHHHHHHHHH")
    quit()
    unittest.main()