.. _api-reference:

API Reference
=============

Working with Merger Trees
-------------------------

The :func:`~ytree.data_structures.load.load` can load all supported
merger tree formats.  Once loaded, the
:func:`~ytree.data_structures.arbor.Arbor.save_arbor` and
:func:`~ytree.data_structures.tree_node.TreeNode.save_tree` functions can be
used to save the entire arbor or individual trees.

.. autosummary::
   :toctree: generated/

   ~ytree.data_structures.load.load
   ~ytree.data_structures.arbor.Arbor
   ~ytree.data_structures.arbor.Arbor.add_alias_field
   ~ytree.data_structures.arbor.Arbor.add_analysis_field
   ~ytree.data_structures.arbor.Arbor.add_derived_field
   ~ytree.data_structures.arbor.Arbor.add_vector_field
   ~ytree.data_structures.arbor.Arbor.save_arbor
   ~ytree.data_structures.arbor.Arbor.select_halos
   ~ytree.data_structures.tree_node.TreeNode
   ~ytree.data_structures.tree_node.TreeNode.save_tree
   ~ytree.data_structures.tree_node_selector.TreeNodeSelector
   ~ytree.data_structures.arbor.Arbor.set_selector
   ~ytree.data_structures.tree_node_selector.TreeNodeSelector
   ~ytree.data_structures.tree_node_selector.add_tree_node_selector
   ~ytree.data_structures.tree_node_selector.max_field_value
   ~ytree.data_structures.tree_node_selector.min_field_value

Visualizing Merger Trees
------------------------

Functionality for plotting merger trees.

.. autosummary::
   :toctree: generated/

   ~ytree.visualization.tree_plot.TreePlot
   ~ytree.visualization.tree_plot.TreePlot.save

.. _internal-classes:

Internal Classes
----------------

Base Classes
############

All frontends inherit from these base classes for arbor, fields,
and i/o.

.. autosummary::
   :toctree: generated/

   ~ytree.data_structures.arbor.Arbor
   ~ytree.data_structures.arbor.CatalogArbor
   ~ytree.data_structures.fields.FieldInfoContainer
   ~ytree.data_structures.fields.FieldContainer
   ~ytree.data_structures.fields.FakeFieldContainer
   ~ytree.data_structures.io.FieldIO
   ~ytree.data_structures.io.TreeFieldIO
   ~ytree.data_structures.io.DefaultRootFieldIO
   ~ytree.data_structures.io.DataFile
   ~ytree.data_structures.io.CatalogDataFile

Arbor Subclasses
################

Arbor subclasses for each frontend.

.. autosummary::
   :toctree: generated/

   ~ytree.frontends.ahf.arbor.AHFArbor
   ~ytree.frontends.consistent_trees.arbor.ConsistentTreesArbor
   ~ytree.frontends.consistent_trees.arbor.ConsistentTreesGroupArbor
   ~ytree.frontends.consistent_trees.arbor.ConsistentTreesHlistArbor
   ~ytree.frontends.consistent_trees_hdf5.arbor.ConsistentTreesHDF5Arbor
   ~ytree.frontends.lhalotree.arbor.LHaloTreeArbor
   ~ytree.frontends.rockstar.arbor.RockstarArbor
   ~ytree.frontends.treefarm.arbor.TreeFarmArbor
   ~ytree.frontends.ytree.arbor.YTreeArbor

FieldInfo Subclasses
####################

Subclasses for frontend-specific field definitions.

.. autosummary::
   :toctree: generated/

   ~ytree.frontends.ahf.fields.AHFFieldInfo
   ~ytree.frontends.consistent_trees.fields.ConsistentTreesFieldInfo
   ~ytree.frontends.consistent_trees_hdf5.fields.ConsistentTreesHDF5FieldInfo
   ~ytree.frontends.lhalotree.fields.LHaloTreeFieldInfo
   ~ytree.frontends.rockstar.fields.RockstarFieldInfo
   ~ytree.frontends.treefarm.fields.TreeFarmFieldInfo

FieldIO Subclasses
##################

Subclasses for data i/o from a whole dataset.

.. autosummary::
   :toctree: generated/

   ~ytree.frontends.ahf.io.AHFDataFile
   ~ytree.frontends.consistent_trees.io.ConsistentTreesTreeFieldIO
   ~ytree.frontends.consistent_trees_hdf5.io.ConsistentTreesHDF5TreeFieldIO
   ~ytree.frontends.consistent_trees_hdf5.io.ConsistentTreesHDF5RootFieldIO
   ~ytree.frontends.lhalotree.io.LHaloTreeTreeFieldIO
   ~ytree.frontends.lhalotree.io.LHaloTreeRootFieldIO
   ~ytree.frontends.ytree.io.YTreeTreeFieldIO
   ~ytree.frontends.ytree.io.YTreeRootFieldIO

DataFile Subclasses
###################

Subclasses for data i/o from individual files.

.. autosummary::
   :toctree: generated/

   ~ytree.frontends.consistent_trees.io.ConsistentTreesDataFile
   ~ytree.frontends.consistent_trees.io.ConsistentTreesHlistDataFile
   ~ytree.frontends.consistent_trees_hdf5.io.ConsistentTreesHDF5DataFile
   ~ytree.frontends.rockstar.io.RockstarDataFile
   ~ytree.frontends.treefarm.io.TreeFarmDataFile
   ~ytree.frontends.ytree.io.YTreeDataFile
