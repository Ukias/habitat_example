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
        elif args.tbsz == "tbOpt":
            tableScaleJsonPath += "/optTableScale.json"            
        f = open(tableScaleJsonPath, "r")        
        jsonDump = f.read()  
        scales = json.loads(jsonDump)              
        self.tbWd = scales["tableWidth"]
        self.tbLg = scales["tableLength"]
        self.tblMidPos = scales["tableMidPosition"]    
        f.close()             
        
    def loadSingleBanana(self, habSim, trnslTble):
        '''
        :param habSim: src.simulator.Simulator
        :param trnslTble: (3,) np.ndarray
        :return: None
        '''
        assert isinstance(habSim.sim, habitat_sim.Simulator)      
        #t = mn.Vector3(self.tblMidPos[0], 1, self.tblMidPos[2]) #manually
        t = mn.Vector3(trnslTble[0], 0.8, trnslTble[2])
        habSim.addYcbObjOnTbl("banana", t)        
        #habSim.saveCurObsv("banana", "banana/")
        #habSim.deleteObjectsOnTable()
        #habSim.saveCurObsv("tbAftDel", "banana/")
    
    def load2Objs(self, habSim):
        assert isinstance(habSim.sim, habitat_sim.Simulator)      
        t = mn.Vector3(self.tblMidPos[0], 1, self.tblMidPos[2])   
        habSim.addYcbObjOnTbl("banana", t)
        t = mn.Vector3(self.tblMidPos[0], 1, self.tblMidPos[2] + 0.2)   
        habSim.addYcbObjOnTbl("cracker_box", t)
        habSim.saveCurObsv("banCb", "banCb/")          
        habSim.deleteObjectsOnTable()
        habSim.saveCurObsv("tbAftDel", "banCb/")         
