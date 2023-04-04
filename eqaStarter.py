from src.simulator import HabitatSimulator
from src.simulatorConfig import *
import argparse

def initializeArgumentParser(data_path):
    parser = argparse.ArgumentParser()    
    #mode parameter
    parser.add_argument(
        '-mode',
        default='simTest',
        type=str,
        choices=['simTest'])     
    
    #scene configuration
    parser.add_argument('-tbsz', default='tbMed', type=str,choices=['tbLg','tbMed', 'tbOpt'])
    
    #image saving
    parser.add_argument('-camPspv', default='front', choices=['brd', 'front'])    
    return(parser)    

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path=dir_path +  "/output/"
    data_path=dir_path + "/data/"

    parser = initializeArgumentParser(data_path)    

    #configuration for simulation
    cfg_settings = default_sim_settings.copy()

    cfg_settings["scene"] = "v3_sc0_staging_00"
    cfg_settings["enable_physics"] = True
    cfg_settings["depth_camera_1stperson"] = True
    cfg_settings["rgba_camera_1stperson"] = True   
    cfg_settings["enable_physics"] = True             
    cfg_settings["data_path"] = data_path
    cfg_settings["output_path"] = output_path	   
	
	#parse arguments	
    args = parser.parse_args()           
    habitatSimulator = HabitatSimulator(cfg_settings,args)        
   
