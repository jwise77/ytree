"""
tests for parallel_trees iterator



"""

#-----------------------------------------------------------------------------
# Copyright (c) ytree development team. All rights reserved.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

import os

from ytree.utilities.testing import ParallelTest, TempDirTest

script_path = os.path.dirname(__file__)

class ParallelTreesTest(TempDirTest, ParallelTest):
    test_script = os.path.join(script_path, "parallel/parallel_trees.py")
    arg_sets = (
        ("forest", 0, 0, 4),
        ("tree",   0, 0, 4),
        ("prog",   0, 0, 4),
        ("forest", 0, 0,  ), # sets save_every to None
        ("forest", 2, 0, 4),
        ("forest", 0, 1, 4),
    )
