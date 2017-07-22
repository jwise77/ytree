"""
ArborArbor io classes and member functions



"""

#-----------------------------------------------------------------------------
# Copyright (c) 2017, Britton Smith <brittonsmith@gmail.com>
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

import h5py
import numpy as np

from ytree.arbor.io import \
    RootFieldIO, \
    TreeFieldIO

class ArborArborTreeFieldIO(TreeFieldIO):
    def _read_fields(self, root_node, fields, dtypes=None,
                     f=None, root_only=False, fcache=None):
        if dtypes is None:
            dtypes = {}

        if fcache is None:
            fcache = {}

        if f is None:
            close = True
            f = h5py.File(self.arbor.filename, "r")
        else:
            close = False

        si = root_node._si
        ei = root_node._ei

        field_data = {}
        fi = self.arbor.field_info
        for field in fields:
            if field not in fcache:
                if field in self.arbor._field_cache:
                    rdata = self.arbor._field_cache[field]
                else:
                    if fi[field].get("vector", False):
                        rfield, ax = field.rsplit("_", 1)
                        rdata = f["data/%s" % rfield][:, "xyz".find(ax)]
                    else:
                        rdata = f["data/%s" % field].value
                    dtype = dtypes.get(field)
                    if dtype is not None:
                        rdata = rdata.astype(dtype)
                    units = fi[field].get("units", "")
                    if units != "":
                        rdata = self.arbor.arr(rdata, units)
                    self.arbor._field_cache[field] = rdata
                fcache[field] = rdata[si:ei]
            field_data[field] = fcache[field]

        if close:
            f.close()

        return field_data

class ArborArborRootFieldIO(RootFieldIO):
    def _read_fields(self, storage_object, fields, dtypes=None):
        if dtypes is None:
            dtypes = {}
        self.arbor.trees

        fcache = storage_object._root_field_data

        fh = h5py.File(self.arbor.filename, "r")
        field_data = {}
        fi = self.arbor.field_info
        for field in fields:
            if field not in fcache:
                if field in self.arbor._field_cache:
                    rdata = self.arbor._field_cache[field]
                else:
                    if fi[field].get("vector", False):
                        rfield, ax = field.rsplit("_", 1)
                        rdata = fh["data/%s" % rfield][:, "xyz".find(ax)]
                    else:
                        rdata = fh["data/%s" % field].value
                    dtype = dtypes.get(field)
                    if dtype is not None:
                        rdata = rdata.astype(dtype)
                    units = fi[field].get("units", "")
                    if units != "":
                        rdata = self.arbor.arr(rdata, units)
                    self.arbor._field_cache[field] = rdata
                fcache[field] = rdata[self.arbor._ri]
            field_data[field] = fcache[field]
        fh.close()

        return field_data
