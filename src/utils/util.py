import magnum as mn
import numpy as np

def rot_3d_x(angle):
	return mn.Matrix3x3(mn.Vector3(1,0,0),mn.Vector3(0,np.cos(angle),-np.sin(angle)),mn.Vector3(0,np.sin(angle),np.cos(angle))).transposed()
	
def rot_3d_y(angle):
	return mn.Matrix3x3(mn.Vector3(np.cos(angle),0,np.sin(angle)),mn.Vector3(0,1,0),mn.Vector3(-np.sin(angle),0,np.cos(angle))).transposed()
	
def rot_3d_z(angle):
	return mn.Matrix3x3(mn.Vector3(np.cos(angle),-np.sin(angle),0),mn.Vector3(np.sin(angle),np.cos(angle),0),mn.Vector3(0,0,1)).transposed()
