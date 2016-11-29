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



if __name__ == "__main__":
    unittest.main()