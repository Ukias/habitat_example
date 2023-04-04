# table mesh issue:

print outputs:
-object handles:  ['frl_apartment_bike_02_:0000', 'frl_apartment_chair_01_:0000', 'frl_apartment_chair_01_:0001', 'frl_apartment_clothes_hanger_02_:0000', 'frl_apartment_indoor_plant_01_:0000', 'frl_apartment_indoor_plant_02_:0000', 'frl_apartment_mat_:0000', 'frl_apartment_picture_01_:0000', 'frl_apartment_rug_01_:0000', 'frl_apartment_rug_02_:0000', 'frl_apartment_sofa_:0000', 'frl_apartment_table_01_:0000', 'frl_apartment_table_02_:0000', 'frl_apartment_table_03_:0000', 'frl_apartment_tv_screen_:0000', 'frl_apartment_tvstand_:0000', 'frl_apartment_wall_cabinet_01_:0000', 'frl_apartment_wall_cabinet_02_:0000']
- table1 mesh top:  0.0
- table1 mesh center:  <bound method PyCapsule.center of Range({0, 0, 0}, {0, 0, 0})>
- table1 mesh_bb:  Range({0, 0, 0}, {0, 0, 0})


# Solved: deletion issue 
method `deleteObjectsOnTable` in `simulator.py`  uses `remove_object_by_handle()` from rigidObjectManager. 
Does not remove object as shown with method `loadSingleBanana` in `clutterLoader.py`. 
Images are saved to folder output/banana.

Objects are from the YCB dataset and the apartment scene is from the replicaCAD dataset.
