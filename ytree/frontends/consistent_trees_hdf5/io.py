"""
ConsistentTreesHDF5Arbor io classes and member functions



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
import os

from ytree.data_structures.io import \
    DataFile, \
    TreeFieldIO
from ytree.frontends.rockstar.io import \
    RockstarDataFile

class ConsistentTreesHDF5DataFile(DataFile):
    def __init__(self, filename, linkname):
        super(ConsistentTreesHDF5DataFile, self).__init__(filename)
        self.linkname = linkname
        self.real_fh = None

    def open(self):
        self.real_fh = h5py.File(self.filename, mode="r")
        self.fh = self.real_fh[self.linkname]

    def close(self):
        self.fh = None
        self.real_fh.close()

class ConsistentTreesHDF5TreeFieldIO(TreeFieldIO):
    def _read_fields(self, root_node, fields, dtypes=None,
                     root_only=False):
        """
        Read fields from disk for a single tree.
        """

        data_file = self.arbor.data_files[root_node._fi]

        if dtypes is None:
            dtypes = {}
        my_dtypes = self._determine_dtypes(
            fields, override_dict=dtypes)

        close = False
        if data_file.fh is None:
            close = True
            data_file.open()
        fh = data_file.fh
        fh.seek(root_node._si)
        if root_only:
            data = [fh.readline()]
        else:
            data = fh.read(
                root_node._ei -
                root_node._si).split("\n")
            if len(data[-1]) == 0:
                data.pop()
        if close:
            data_file.close()

        nhalos = len(data)
        field_data = {}
        fi = self.arbor.field_info
        for field in fields:
            field_data[field] = np.empty(nhalos, dtype=my_dtypes[field])

        for i, datum in enumerate(data):
            ldata = datum.strip().split()
            if len(ldata) == 0: continue
            for field in fields:
                dtype = my_dtypes[field]
                field_data[field][i] = dtype(ldata[fi[field]["column"]])

        for field in fields:
            units = fi[field].get("units", "")
            if units != "":
                field_data[field] = \
                  self.arbor.arr(field_data[field], units)

        return field_data
