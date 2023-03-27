import habitat_sim
import magnum as mn
import numpy as np
import json
from src.simulator import *
from src.utils.util import rot_3d_x, rot_3d_y, rot_3d_z

class ClutterLoader:
    def __init__(self,args, habSim):
        tableScaleJsonPath = habSim.data_path
        if args.tbsz == "tbLg":
            tableScaleJsonPath += "/largeTableScale.json"
        elif args.tbsz == "tbMed":
            tableScaleJsonPath += "/mediumTableScale.json"
        f = open(tableScaleJsonPath, "r")        
        jsonDump = f.read()  
        scales = json.loads(jsonDump)              
        self.tbWd = scales["tableWidth"]
        self.tbLg = scales["tableLength"]
        self.tblMidPos = scales["tableMidPosition"]    
        f.close()             
        
    def loadSingleBanana(self, habSim):
        assert isinstance(habSim.sim, habitat_sim.Simulator)      
        t = mn.Vector3(self.tblMidPos[0], 1, self.tblMidPos[2])          
        habSim.addYcbObjOnTbl("banana", t)
        habSim.sim.agents[0].scene_node.translation = t
        habSim.sim.agents[0].scene_node.translate(mn.Vector3(0,1,-0.5))
        habSim.sim.agents[0].scene_node.rotation = mn.Quaternion.from_matrix(habSim.sim.agents[0].scene_node.rotation.normalized().to_matrix() @ rot_3d_x(np.pi/2))        
        habSim.save_as_image(habSim.sim.get_sensor_observations(), "banana", "banana/",True)  
        habSim.deleteObjectsOnTable()
        habSim.save_as_image(habSim.sim.get_sensor_observations(), "tbAftDel", "banana/",True)         
