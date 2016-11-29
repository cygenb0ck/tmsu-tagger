#!/usr/bin/env bash
./tests.py

sudo umount -l ./test_data/mp
rm -rf ./test_data/.tmsu