import habitat_sim
import numpy as np
import os
    
camera_resolution = [544, 720]

default_sim_settings = {
	# settings shared by example.py and benchmark.py
	"camera_resolution": camera_resolution,
    "max_frames": 1000,
    "width": 640,
    "height": 480,
    "default_agent": 0,
    "sensor_height": 1.5,
    "hfov": 90,
    "rgba_camera_3rdperson": True,  # RGB sensor (default: ON)
    "semantic_sensor": False,  # semantic sensor (default: OFF)
    "depth_sensor": False,  # depth sensor (default: OFF)
    "ortho_rgba_sensor": False,  # Orthographic RGB sensor (default: OFF)
    "ortho_depth_sensor": False,  # Orthographic depth sensor (default: OFF)
    "ortho_semantic_sensor": False,  # Orthographic semantic sensor (default: OFF)
    "fisheye_rgba_sensor": False,
    "fisheye_depth_sensor": False,
    "fisheye_semantic_sensor": False,
    "equirect_rgba_sensor": False,
    "equirect_depth_sensor": False,
    "equirect_semantic_sensor": False,
    "rgba_camera_1stperson": False,
    "depth_camera_1stperson": False,
    "seed": 1,
    "silent": False,  # do not print log info (default: OFF)
    # settings exclusive to example.py
    "save_png": False,  # save the pngs to disk (default: OFF)
    "print_semantic_scene": False,
    "print_semantic_mask_stats": False,
    "compute_shortest_path": False,
    "compute_action_shortest_path": False,
    #"scene": "data/scene_datasets/habitat-test-scenes/skokloster-castle.glb",
    #"scene": "NONE",
    "scene": "apt_3",
    "test_scene_data_url": "http://dl.fbaipublicfiles.com/habitat/habitat-test-scenes.zip",
    "scene_dataset_config_file": "data/replica_cad/replicaCAD.scene_dataset_config.json",
    "goal_position": [5.047, 0.199, 11.145],
    "enable_physics": False,
    "enable_gfx_replay_save": False,
    "physics_config_file": "./data/default.physics_config.json",
    "num_objects": 10,
    "test_object_index": 0,
    "frustum_culling": True,
    }    

class SimConfigurator:
    def make_cfg(self, settings):
        # settings: class
        sim_cfg = habitat_sim.SimulatorConfiguration()
        if "scene_dataset_config_file" in settings:
            sim_cfg.scene_dataset_config_file = settings["scene_dataset_config_file"]
        sim_cfg.frustum_culling = settings.get("frustum_culling", False)
        if "enable_physics" in settings:
            sim_cfg.enable_physics = settings["enable_physics"]
        if "physics_config_file" in settings:
            sim_cfg.physics_config_file = settings["physics_config_file"]
        if not settings["silent"]:
            print("sim_cfg.physics_config_file = " + sim_cfg.physics_config_file)
        if "scene_light_setup" in settings:
            sim_cfg.scene_light_setup = settings["scene_light_setup"]
        sim_cfg.gpu_device_id = 0
        if not hasattr(sim_cfg, "scene_id"):
            raise RuntimeError(
				"Error: Please upgrade habitat-sim. SimulatorConfig API version mismatch"
            )
        sim_cfg.scene_id = settings["scene"]

		# define default sensor parameters (see src/esp/Sensor/Sensor.h)
        sensor_specs = []

        def create_camera_spec(**kw_args):
            camera_sensor_spec = habitat_sim.CameraSensorSpec()
            camera_sensor_spec.sensor_type = habitat_sim.SensorType.COLOR
            camera_sensor_spec.resolution = [settings["height"], settings["width"]]
            camera_sensor_spec.position = [0, settings["sensor_height"], 0]
            for k in kw_args:
                setattr(camera_sensor_spec, k, kw_args[k])
            return camera_sensor_spec

        if settings["rgba_camera_3rdperson"]:
            color_sensor_spec = create_camera_spec(
                uuid="rgba_camera_3rdperson",
				position=[0.0, 1.0, 0.3],
				rotation=[0.0, 0.0, 0.0],
				hfov=settings["hfov"],
				sensor_type=habitat_sim.SensorType.COLOR,
				sensor_subtype=habitat_sim.SensorSubType.PINHOLE,
			)
            sensor_specs.append(color_sensor_spec)

        if settings["rgba_camera_1stperson"]:
            rgba_camera_1stperson_spec = habitat_sim.CameraSensorSpec()
            rgba_camera_1stperson_spec.uuid = "rgba_camera_1stperson"
            rgba_camera_1stperson_spec.sensor_type = habitat_sim.SensorType.COLOR
            rgba_camera_1stperson_spec.resolution = settings["camera_resolution"]
            rgba_camera_1stperson_spec.position = [0.0, 0.6, 0.0]
            #rgba_camera_1stperson_spec.orientation = [-np.pi/2, 0.0, 0.0] # for bird's eye perspective on table
            rgba_camera_1stperson_spec.orientation = [0.0, np.pi, 0.0] #for first person camera
            rgba_camera_1stperson_spec.sensor_subtype = habitat_sim.SensorSubType.PINHOLE
            sensor_specs.append(rgba_camera_1stperson_spec)

        if settings["depth_camera_1stperson"]:
            depth_camera_1stperson_spec = habitat_sim.CameraSensorSpec()
            depth_camera_1stperson_spec.uuid = "depth_camera_1stperson"
            depth_camera_1stperson_spec.sensor_type = habitat_sim.SensorType.DEPTH
            depth_camera_1stperson_spec.resolution = settings["camera_resolution"]
            depth_camera_1stperson_spec.position = [0.0, 0.6, 0.0]
            depth_camera_1stperson_spec.orientation = [0.0, np.pi, 0.0]
            depth_camera_1stperson_spec.sensor_subtype = habitat_sim.SensorSubType.PINHOLE
            sensor_specs.append(depth_camera_1stperson_spec)		

		# create agent specifications
        agent_cfg = habitat_sim.agent.AgentConfiguration()
        agent_cfg.sensor_specifications = sensor_specs
        agent_cfg.action_space = {
            "move_forward": habitat_sim.agent.ActionSpec(
                "move_forward", habitat_sim.agent.ActuationSpec(amount=0.25)
            ),
            "turn_left": habitat_sim.agent.ActionSpec(
                "turn_left", habitat_sim.agent.ActuationSpec(amount=10.0)
            ),
            "turn_right": habitat_sim.agent.ActionSpec(
                "turn_right", habitat_sim.agent.ActuationSpec(amount=10.0)
            ),
        }

		# override action space to no-op to test physics
        if sim_cfg.enable_physics:
            agent_cfg.action_space = {
                "move_forward": habitat_sim.agent.ActionSpec(
                    "move_forward", habitat_sim.agent.ActuationSpec(amount=0.0)
                )
            }

        return habitat_sim.Configuration(sim_cfg, [agent_cfg])      
