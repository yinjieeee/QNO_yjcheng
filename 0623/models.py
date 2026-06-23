#models.py

import meep as mp
import config as cfg
import numpy as np


def build_scene_data(config_dict):
    WS2 = mp.Medium(index=2.4)
    gap = mp.Medium(index=3.31)
    diamond = mp.Medium(index=2.4)
    air = mp.air
    
    cell_size = mp.Vector3(config_dict['Sx'], 
                           config_dict['Sy'],
                           config_dict['Sz'])
    
    design_center = mp.Vector3(0, 0, -config_dict['Sz']/2 + config_dict['base_thick'] + config_dict['tmd_thick'] + config_dict['design_thick']/2)

    tmd_center = mp.Vector3(0, 0, -config_dict['Sz']/2 + config_dict['base_thick'] + config_dict['tmd_thick']/2)

    base_center = mp.Vector3(0, 0, -config_dict['Sz']/2 + config_dict['base_thick']/2)
    
    Nx = int(config_dict['resolution'] * config_dict['design_width']) + 1
    Ny = int(config_dict['resolution'] * config_dict['design_height']) + 1
    design_var = mp.MaterialGrid(mp.Vector3(Nx, Ny, 1), mp.air, gap, grid_type="U_MEAN")

    #pml_layer=[mp.PML(config_dict['dpml'], direction=mp.Z)]
    pml_layer=[mp.PML(config_dict['dpml'])]
    geometry = [
        mp.Block(center=design_center,
                 size=mp.Vector3(config_dict['design_width'], config_dict['design_height'], config_dict['design_thick']),
                 material=design_var),
        mp.Block(center=tmd_center,
                 size=mp.Vector3(config_dict['design_width'], config_dict['design_height'], config_dict['tmd_thick']),
                 material=WS2),
        mp.Block(center=base_center,
                 size=mp.Vector3(config_dict['design_width'], config_dict['design_height'], config_dict['base_thick']),
                 material=diamond)
    ]


    src_z = -config_dict['Sz']/2 + config_dict['base_thick'] + config_dict['tmd_thick']/2
    src_center = mp.Vector3(0, 0, src_z)

    w0 = config_dict.get('w0_target', 0.5)

    #def gaussian_amp(pt):
    #    r2 = pt.x**2 + pt.y**2
    #    return np.exp(-r2 / (2 * w0**2))   # 只回傳實數振幅分布

    src = mp.GaussianSource(config_dict['frequency'], fwidth=config_dict['fwidth'])
    src_size = mp.Vector3(0, 0, 0)
    
    source = [
        mp.Source(src, component=mp.Ex, center=src_center, size=src_size, amplitude=1.0),
        mp.Source(src, component=mp.Ey, center=src_center, size=src_size, amplitude=1j)
    ]


    monitor_z = config_dict['Sz']/2 - config_dict['dpml'] - config_dict['monitor_pml']
    
    return {
        "cell_size": cell_size,
        "geometry": geometry,
        "sources": source,
        "pml_layer": pml_layer,
        "design_center": design_center,
        "monitor_z": monitor_z
    }