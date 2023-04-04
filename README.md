# table mesh issue:

Banana has to be placed exactly on table1. Table is placed in the scene but outputs of table1 mesh center and mesh_top are wrong:

print outputs in constructor of class `HabitatSimulator` in `src/simulator.py`:
- object handles:  [..., 'frl_apartment_table_01_:0000', 'frl_apartment_table_02_:0000', 'frl_apartment_table_03_:0000', 'frl_apartment_tv ...]
- table1 mesh top:  0.0
- table1 mesh center:  <bound method PyCapsule.center of Range({0, 0, 0}, {0, 0, 0})>
- table1 mesh_bb:  Range({0, 0, 0}, {0, 0, 0})

Objects are from the YCB dataset and the apartment scene is from the replicaCAD dataset.

# Solved: deletion issue 
method `deleteObjectsOnTable` in `simulator.py`  uses `remove_object_by_handle()` from rigidObjectManager. 
Does not remove object as shown with method `loadSingleBanana` in `clutterLoader.py`. 
Images are saved to folder output/banana.

Objects are from the YCB dataset and the apartment scene is from the replicaCAD dataset.
