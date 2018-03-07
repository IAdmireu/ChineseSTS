#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#
# Copyright (c) 2017 <> All Rights Reserved
#
#
# File: /Users/hain/ai/ChineseSTS/app/eval.py
# Author: Hai Liang Wang
# Date: 2018-03-07:10:06:11
#
#===============================================================================

"""
   
"""
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 . All Rights Reserved"
__author__    = "Hai Liang Wang"
__date__      = "2018-03-07:10:06:11"


import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # raise "Must be using Python 3"

# Get ENV
ENVIRON = os.environ.copy()

from absl import flags   #absl-py
from absl import logging #absl-py

FLAGS = flags.FLAGS

import synonyms
from tqdm import tqdm
import unittest


def append_line_to_file(file, line):
    with open(file, "a") as fout:
        fout.write(line)

# run testcase: python /Users/hain/ai/ChineseSTS/app/eval.py Test.testExample
class Test(unittest.TestCase):
    '''
    
    '''
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_eval_synonyms(self):
        logging.info("test_eval_synonyms")
        from_ = os.path.join(curdir, os.path.pardir, "data", "simtrain_to05sts.txt")
        to_ = os.path.join(curdir, os.path.pardir, "data", "synonyms_eval.txt")
        if os.path.exists(to_): os.remove(to_)
        append_line_to_file(to_, "# [synonyms](https://github.com/huyingxi/Synonyms) v(%s) 相似度评测 \n" % synonyms.__version__)
        append_line_to_file(to_, "评测数据源: https://github.com/IAdmireu/ChineseSTS \n \n")
        append_line_to_file(to_, "置信区间 [0,5]，分数越高越相似 \n")
        append_line_to_file(to_, "| %s | %s | %s | %s | %s | %s | \n" % ("句子A ID", "句子A", "句子B ID", "句子 B", "标注分数", "预测分数"))
        append_line_to_file(to_, "| --- | --- | --- | --- | --- | --- | \n")
        with open(from_, "r") as fin:
            for x in tqdm(list(fin.readlines())):
                o = x.strip().split("\t")
                if len(o) == 5:
                    yid, yc, zid, zc, yzs = o
                    syn_score = synonyms.compare(yc, zc) * 5.0
                    # print("%s | %s => %s | %s" % (yc, zc, yzs, syn_score))
                    append_line_to_file(to_, "| %s | %s | %s | %s | %s | %.3f | \n" % (yid, yc, zid, zc, yzs, syn_score))
                
def test():
    unittest.main()

if __name__ == '__main__':
    FLAGS([__file__, '--verbosity', '1']) # DEBUG 1; INFO 0; WARNING -1
    test()
