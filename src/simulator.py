import habitat_sim
import magnum as mn
import numpy as np
from src.utils.util import rot_3d_x, rot_3d_y, rot_3d_z
from src.clutterLoader import *
from src.simulatorConfig import SimConfigurator
import habitat_sim.utils.viz_utils as vut
import os

class HabitatSimulator:
    def __init__(self, simCfgSettings, args):
		# simCfgSettings: dict
		# args: class
        simConfigurator = SimConfigurator()   
        hab_cfg = simConfigurator.make_cfg(simCfgSettings)
        self.data_path = simCfgSettings["data_path"]
        self.output_path = simCfgSettings["output_path"]
        self.objectsOnTable = {}
        self.clutterLoader = ClutterLoader(args, self)

        with habitat_sim.Simulator(hab_cfg) as sim:
            self.sim = sim
            # get the rigid object manager
            rigid_obj_mgr = self.sim.get_rigid_object_manager()            
			#load the full YCB dataset into the MetadataMediator
            sim.metadata_mediator.active_dataset = self.data_path + "hab_ycb_v1.2/ycb.scene_dataset_config.json"		
		
			# get the physics object attributes manager
            obj_templates_mgr = sim.get_object_template_manager()                                  
            
            if args.mode == 'simTest':
                self.loadSingleBanana()
                
    def save_as_image(self,observation, filename, foldername="", outputFolder=True):
        if outputFolder == True and not os.path.exists(self.output_path + foldername):
            os.mkdir(self.output_path + foldername)  
        elif outputFolder == False and not os.path.exists(self.data_path + foldername):
            os.mkdir(self.data_path + foldername)  			
        im = vut.observation_to_image(observation["rgba_camera_1stperson"], "color")
        if outputFolder==True:
            im.save(self.output_path + foldername + filename + ".png")
        elif outputFolder == False:
            im.save(self.data_path + foldername + filename + ".png")     
            
    def simulate(self, dt, makeVideo):
        assert isinstance(self.sim, habitat_sim.Simulator)
        observations=[]
        start_time = self.sim.get_world_time()
        while self.sim.get_world_time() < start_time + dt:
            self.sim.step_physics(1.0 / 60.0)
            if makeVideo == True:
                observations.append(self.sim.get_sensor_observations())  	
        return(observations)
        
    def deleteObjectsOnTable(self):
        for handle in self.objectsOnTable.keys():
            self.sim.get_rigid_object_manager().remove_object_by_handle(handle)  
            
    def addYcbObjOnTbl(self, tmplHName, transl):
		# tmplHName: str
		# transl: mn.Vector3
        obj_mgr = self.sim.get_object_template_manager()	
        obj = self.sim.get_rigid_object_manager().add_object_by_template_handle(obj_mgr.get_template_handles(tmplHName)[0]) 
        obj.translation = transl
        if tmplHName in self.objectsOnTable.keys():
            self.objectsOnTable[tmplHName]+=1
        else:
            self.objectsOnTable[tmplHName] = 1 
        obj.collidable = True
        obj.motion_type = habitat_sim.physics.MotionType.KINEMATIC                   
            
    def loadSingleBanana(self):                  
        self.clutterLoader.loadSingleBanana(self)
                                            
