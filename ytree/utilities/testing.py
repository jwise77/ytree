"""
testing utilities



"""

#-----------------------------------------------------------------------------
# Copyright (c) ytree development team. All rights reserved.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

import h5py
import numpy as np
from numpy.testing import \
    assert_equal, \
    assert_array_equal
import os
import shutil
import tempfile
from unittest import \
    TestCase
from yt.testing import \
    assert_rel_equal
from yt.funcs import \
    get_pbar

from ytree.data_structures.arbor import \
    load
from ytree.frontends.ytree import \
    YTreeArbor
from ytree.config import \
    ytreecfg

if "YTREE_TEST_DATA_DIR" in os.environ:
    test_data_dir = os.environ["YTREE_TEST_DATA_DIR"]
else:
    test_data_dir = ytreecfg["ytree"].get("test_data_dir", ".")
generate_results = \
  int(os.environ.get("YTREE_GENERATE_TEST_RESULTS", 0)) == 1

def requires_file(req_file):

    def ffalse(func):
        return None

    def ftrue(func):
        return func

    if os.path.exists(req_file):
        return ftrue
    else:
        return ffalse

class TempDirTest(TestCase):
    """
    A test class that runs in a temporary directory and
    removes it afterward.
    """

    def setUp(self):
        self.curdir = os.getcwd()
        self.tmpdir = tempfile.mkdtemp()
        os.chdir(self.tmpdir)

    def tearDown(self):
        os.chdir(self.curdir)
        shutil.rmtree(self.tmpdir)

class ArborTest(object):
    """
    Do some standard tests on an arbor.
    """

    arbor_type = None
    test_filename = None
    num_data_files = None
    tree_skip = 1

    _arbor = None
    @property
    def arbor(self):
        if self._arbor is None:
            if not os.path.exists(self.test_filename):
                test_filename = \
                  os.path.join(test_data_dir, self.test_filename)
                if os.path.exists(test_filename):
                    self.test_filename = test_filename
                else:
                    self.skipTest("test file missing")
            self._arbor = load(self.test_filename)
        return self._arbor

    def test_arbor_type(self):
        assert isinstance(self.arbor, self.arbor_type)

    def test_data_files(self):
        if self.num_data_files is None:
            return
        assert_equal(
            len(self.arbor.data_files), self.num_data_files,
            err_msg='Incorrect number of data files for %s.' % self.arbor)

    def test_save_and_reload(self):
        save_and_compare(self.arbor, skip=self.tree_skip)

    def test_vector_fields(self):
        a = self.arbor
        t = a[0]
        for field in a.field_info.vector_fields:

            magfield = np.sqrt((a[field]**2).sum(axis=1))
            assert_array_equal(a["%s_magnitude" % field], magfield)

            for i, ax in enumerate("xyz"):
                assert_array_equal(
                    a["%s_%s" % (field, ax)],
                    a[field][:, i])

                assert_array_equal(
                    t["%s_%s" % (field, ax)],
                    t[field][i])

                for group in ["prog", "tree"]:
                    assert_array_equal(
                        t[group, "%s_%s" % (field, ax)],
                        t[group, field][:, i])

def save_and_compare(arbor, skip=1):
    """
    Check that arbor saves correctly.
    """

    if skip > 1:
        trees = arbor[::skip]
    else:
        trees = None

    fn = arbor.save_arbor(trees=trees)
    save_arbor = load(fn)
    assert isinstance(save_arbor, YTreeArbor)
    compare_arbors(save_arbor, arbor, skip2=skip)

def compare_arbors(a1, a2, groups=None, fields=None, skip1=1, skip2=1):
    """
    Compare all fields for all trees in two arbors.
    """

    if groups is None:
        groups = ["tree", "prog"]

    if fields is None:
        fields = a1.field_list

    for field in fields:
        assert (a1[field][::skip1] == a2[field][::skip2]).all()

    trees1 = a1[::skip1]
    trees2 = a2[::skip2]

    ntot = trees1.size
    pbar = get_pbar("Comparing trees", ntot)
    for t1, t2 in zip(trees1, trees2):
        compare_trees(t1, t2, groups=groups, fields=fields)
        pbar.update(1)
    pbar.finish()

def compare_trees(t1, t2, groups=None, fields=None):
    """
    Compare all fields between two trees.
    """

    if groups is None:
        groups = ["tree", "prog"]

    if fields is None:
        fields = t1.arbor.field_list

    for field in fields:
        for group in groups:
            assert_array_equal(
                t1[group, field], t2[group, field],
                err_msg="Tree comparison failed for %s field: %s." %
                (group, field))
    t1.arbor.reset_node(t1)
    t2.arbor.reset_node(t2)

def compare_hdf5(fh1, fh2, compare=None, compare_groups=True,
                 **kwargs):
    """
    Compare all datasets between two hdf5 files.
    """

    if compare is None:
        compare = assert_array_equal
    if not isinstance(fh1, h5py.Group):
        fh1 = h5py.File(fh1, "r")
    if not isinstance(fh2, h5py.Group):
        fh2 = h5py.File(fh2, "r")

    if compare_groups:
        assert sorted(list(fh1.keys())) == sorted(list(fh2.keys())), \
          "%s and %s have different datasets in group %s." % \
          (fh1.file.filename, fh2.file.filename, fh1.name)

    for key in fh1.keys():
        if isinstance(fh1[key], h5py.Group):
            compare_hdf5(fh1[key], fh2[key],
                         compare_groups=compare_groups,
                         compare=compare, **kwargs)
        else:
            err_msg = "%s field not equal for %s and %s" % \
              (key, fh1.file.filename, fh2.file.filename)
            if fh1[key].dtype == "int":
                assert_array_equal(fh1[key][()], fh2[key][()],
                                   err_msg=err_msg)
            else:
                compare(fh1[key][()], fh2[key][()],
                        err_msg=err_msg, **kwargs)

def assert_array_rel_equal(a1, a2, decimals=16, **kwargs):
    """
    Wraps assert_rel_equal with, but decimals is a keyword arg.
    """
    assert_rel_equal(a1, a2, decimals, **kwargs)
