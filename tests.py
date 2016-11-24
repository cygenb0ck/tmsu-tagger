#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import shutil

import tagger

data_dir = "./test_data"

class TestTMSUInit(unittest.TestCase):
    def setUp(self):
        self.tmsu_dir = data_dir + "/.tmsu"
        self._remove_tmsu()

    def tearDown(self):
        self._remove_tmsu()

    def _remove_tmsu(self):
        if os.path.exists(self.tmsu_dir):
            shutil.rmtree(self.tmsu_dir)

    def test_init(self):
        tagger.init_tmsu(data_dir)
        self.assertTrue(os.path.isdir(self.tmsu_dir))
        self.assertTrue(os.path.exists(self.tmsu_dir+"/db"))


if __name__ == "__main__":
    unittest.main()