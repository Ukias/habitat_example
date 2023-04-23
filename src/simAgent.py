from src.utils.util import *
import json

class SimAgent:	
    def __init__(self, habSim, args, height):
        self.habSim = habSim  
        tableScaleJsonPath = habSim.data_path
        if args.tbsz == "tbLg":
            tableScaleJsonPath += "/largeTableScale.json"
        elif args.tbsz == "tbMed":
            tableScaleJsonPath += "/mediumTableScale.json"
        elif args.tbsz == "tbOpt":
            tableScaleJsonPath += "/optTableScale.json"
        f = open(tableScaleJsonPath, "r")        
        jsonDump = f.read()  
        scales = json.loads(jsonDump)              
        tblMidPos = scales["tableMidPosition"]         
        self.initRot = habSim.sim.agents[0].scene_node.rotation
        if args.camPspv == 'brd':
            habSim.sim.agents[0].scene_node.translation = tblMidPos
            habSim.sim.agents[0].scene_node.translate(mn.Vector3(0,1.5,-0.5))
            habSim.sim.agents[0].scene_node.rotation = mn.Quaternion.from_matrix(habSim.sim.agents[0].scene_node.rotation.normalized().to_matrix() @ rot_3d_x(np.pi/2))  
        elif args.camPspv == 'front':
            tblMidPos = mn.Vector3(tblMidPos[0], tblMidPos[1], tblMidPos[2])
            self.habSim.sim.agents[0].scene_node.translation = tblMidPos + mn.Vector3(-0.5,0,-2)
            self.habSim.sim.agents[0].scene_node.translation[1] = height
            self.habSim.sim.agents[0].scene_node.rotation = self.initRot
        
