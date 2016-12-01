import numpy as np
import os
from yt.testing import \
    requires_file
from ytree.arbor import \
    ArborArbor, \
    ConsistentTreesArbor, \
    load
from ytree.utilities.testing import \
    compare_arbors, \
    get_test_data_dir, \
    in_tmpdir

CT = os.path.join(get_test_data_dir(),
                  "100Mpc_64/dm_enzo/rockstar_halos/trees/tree_0_0_0.dat")

@in_tmpdir
@requires_file(CT)
def test_ct_arbor():
    a1 = load(CT)
    assert isinstance(a1, ConsistentTreesArbor)
    m1 = a1["mvir"]

    fn = a1.save_arbor("arbor_ct.h5")
    a2 = load(fn)
    assert isinstance(a2, ArborArbor)
    m2 = a2["mvir"]

    assert (m1 == m2).all()
    compare_arbors(a1, a2)

    i1 = np.argsort(m1.d)[::-1][0]
    fn = a1[i1].save_tree()
    a3 = load(fn)
    assert isinstance(a3, ArborArbor)
    for field in a1.field_list:
        assert (a1[i1]["tree", field] == a3[0]["tree", field]).all()
