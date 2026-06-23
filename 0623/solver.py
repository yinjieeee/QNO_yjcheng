#solver.py

import numpy as np
import meep as mp
import meep.adjoint as mpa
import nlopt
import csv
import os
from autograd import tensor_jacobian_product
import utils
import models
import physics
import time

class LGOptimizer:
    def __init__(self, cfg, mapping):
        self.cfg = cfg
        self.field_cache = {'near_fields': None, 'ff_fields': None}
        self.beta_checkpoints = []
        self.config_dict = {
            'resolution':         cfg.resolution,
            'design_width':       cfg.design_width,
            'design_height':      cfg.design_height,
            'design_thick':       cfg.design_thick,
            'tmd_width':          cfg.tmd_width,
            'tmd_height':         cfg.tmd_height,
            'tmd_thick':          cfg.tmd_thick,
            'base_width':         cfg.base_width,
            'base_height':        cfg.base_height,
            'base_thick':         cfg.base_thick,
            'source_material':    cfg.source_material,
            'material_monitor':   cfg.material_monitor,
            'monitor_pml':        cfg.monitor_pml,
            'Sx':                 cfg.Sx,
            'Sy':                 cfg.Sy,
            'Sz':                 cfg.Sz,
            'dpml':               cfg.dpml,
            'frequency':          cfg.frequency,
            'fwidth':             cfg.fwidth,
            'eta_i':              cfg.eta_i,
            'eta_e':              cfg.eta_e,
            'wavelength':         cfg.wavelength,
            'monitor_z':          cfg.monitor_z,
            'src_z':              cfg.src_z,
            'far_field_distance': cfg.far_field_distance,
            'ff_width':           cfg.ff_width,
            'ff_res':             cfg.ff_res,
            'l_charge':           cfg.l_charge,
            'p_radial':           cfg.p_radial,
            'w0_target':          cfg.w0_target,
            'w0_radius':          cfg.w0_radius,
            'zR':                 cfg.zR,
            'z_ff_total':         cfg.z_ff_total,
        }
        self.best_snapshot = {
            'x'               : None,
            'mapped_x'        : None,
            'fom'             : -np.inf,
            'iter'            : None,
            'near_fields'     : None,
            'ff_fields'       : None,
            'overlap'         : None,
            'purity'          : None,
        }
        self.mapping = mapping

        self.cur_iter = [0]
        self.current_beta = 1.0
        self.history_FOM = []
        self.history_overlap = []
        self.history_purity = []

        self.obj_csv_path = os.path.join(cfg.dir_path, "objective_evolution.csv")
        if mp.am_master():
            utils.init_csv(self.obj_csv_path, ["Iteration", "Beta", "Raw_Purity", "Overlap_Abs2", "FOM"])

        scene = models.build_scene_data(self.config_dict)

        self.monitor_z  = scene['monitor_z']
        self.design_center = scene['design_center']
        self.design_size = mp.Vector3(
            self.config_dict['design_width'],
            self.config_dict['design_height'],
            self.config_dict['design_thick']
        )

        self.Nx = int(self.config_dict['resolution'] * self.config_dict['design_width']) + 1
        self.Ny = int(self.config_dict['resolution'] * self.config_dict['design_height']) + 1
        self.design_var = scene['geometry'][0].material

        design_region = mpa.DesignRegion(
            self.design_var,
            volume=mp.Volume(
                center=scene['design_center'],
                size=mp.Vector3(
                    self.config_dict['design_width'],
                    self.config_dict['design_height'],
                    self.config_dict['design_thick']
                )
            )
        )
        self.grid_shape = (self.Nx, self.Ny, 1)

        k_point = mp.Vector3(0, 0, 0)
        self.sim = mp.Simulation(
            cell_size=scene['cell_size'],
            geometry=scene['geometry'],
            sources=scene['sources'],
            boundary_layers=scene['pml_layer'],
            resolution=self.config_dict['resolution'],
            default_material=mp.air,
            force_complex_fields=True,
            k_point=k_point
        )

        def custom_update(params):
            shaped_params = params.reshape(self.Nx, self.Ny, 1)
            checked = self.design_var.check_weights(shaped_params)
            self.design_var.weights = checked.astype(np.float64)

        design_region.update_design_parameters = custom_update

        self.plot_sim = mp.Simulation(
            cell_size=scene['cell_size'],
            geometry=scene['geometry'],
            boundary_layers=scene['pml_layer'],
            resolution=self.config_dict['resolution'],
            default_material=mp.air,
            force_complex_fields=True,
            k_point=k_point
        )

        self.opt_problem = physics.create_opt_problem(
            self.sim, design_region, self.config_dict, field_cache=self.field_cache
        )




    def objective(self, x, grad):
        self.cur_iter[0] += 1
        start_time = time.time()

        mapped_x = self.mapping(x, self.config_dict['eta_i'], self.current_beta)
        f0, dJ_du = self.opt_problem([mapped_x])
            
        elapsed = time.time() - start_time

        if grad.size > 0:
            gradient = tensor_jacobian_product(self.mapping, 0)(
                x, self.config_dict['eta_i'], self.current_beta, dJ_du
            )
            grad[:] = gradient
            if mp.am_master():
                print(f"Iter {self.cur_iter[0]} | Beta {self.current_beta:.2f} | "
                      f"FOM: {-f0:.6f} | Grad Norm: {np.linalg.norm(grad):.6e}")

        current_FOM = -float(f0)
        self.history_FOM.append(current_FOM)

        
            
        current_overlap = self.opt_problem.field_cache.get('overlap_abs2', float('nan'))
        self.history_overlap.append(current_overlap)
        current_purity = self.opt_problem.field_cache.get('purity', float('nan'))
        self.history_purity.append(current_purity)
        
        # best iter for each beta
        if current_FOM > self.best_snapshot['fom']:
            self.best_snapshot['x']       = x.copy()
            self.best_snapshot['mapped_x']= mapped_x.copy()
            self.best_snapshot['fom']     = current_FOM
            self.best_snapshot['iter']    = self.cur_iter[0]
            self.best_snapshot['overlap'] = current_overlap
            self.best_snapshot['purity']  = current_purity

            if mp.am_master():
                near_cached = self.opt_problem.field_cache.get('near_fields')
                ff_cached   = self.opt_problem.field_cache.get('ff_fields')
                self.best_snapshot['near_fields'] = (
                    {k: v.copy() for k, v in near_cached.items()} if near_cached else None
                )
                self.best_snapshot['ff_fields'] = (
                    {k: v.copy() for k, v in ff_cached.items()} if ff_cached else None
                )
            
        if mp.am_master():
            utils.append_csv(self.obj_csv_path,
                             [self.cur_iter[0], self.current_beta, current_purity, current_overlap, current_FOM])
            print(f"Iter {self.cur_iter[0]} | Beta {self.current_beta:.2f} | Purity: {current_purity:.6f} "
                  f"Overlap_abs2: {current_overlap} | (Best FoM: {max(self.history_FOM):.6f})")
            print(f'Time: {elapsed:.2f}s')

        return float(f0)

    def optimize(self, x_init, beta_schedule, nlopt_params):
        x = x_init.copy()

        for beta in beta_schedule:
            self.current_beta = beta
            self.best_fom_this_beta = -np.inf
            self.best_x_this_beta = None

            self.best_snapshot = {
                'x'               : None,
                'mapped_x'        : None,
                'fom'             : -np.inf,
                'iter'            : None,
                'near_fields'     : None,
                'ff_fields'       : None,
                'overlap'         : None,
                'purity'          : None,
            }


            
            if mp.am_master():
                print(f"\n--- Starting Beta Stage: {beta} ---")

            solver = nlopt.opt(nlopt_params['algorithm'], len(x))
            solver.set_min_objective(self.objective)
            #solver.set_ftol_rel(nlopt_params['ftol'])

            if beta < 32.0:
                current_maxeval = 12
            elif 32.0 <= beta <= 1024.0:
                current_maxeval = 1
            else:
                current_maxeval = nlopt_params['update_factor']
            solver.set_maxeval(current_maxeval)
            
            solver.set_lower_bounds(nlopt_params['lb'])
            solver.set_upper_bounds(nlopt_params['ub'])

            try:
                x = solver.optimize(x)
            except nlopt.RoundoffLimited:
                if mp.am_master():
                    print("NLopt: Roundoff limited, moving to next stage.")
            except nlopt.ForcedStop:
                if mp.am_master():
                    print("NLopt: Forced stop.")

            self.beta_checkpoints.append(self.cur_iter[0])

            # 直接從最佳快照提取數據，完全不需重跑模擬
            snap        = self.best_snapshot
            best_x      = snap['x'] if snap['x'] is not None else x
            mapped_x    = snap['mapped_x']
            near_fields = snap['near_fields']
            ff_fields   = snap['ff_fields']
            best_iter   = snap['iter']
            
            # use best iter for plotting
            #best_x = self.best_x_this_beta if self.best_x_this_beta is not None else x
            #mapped_x = self.mapping(best_x, self.config_dict['eta_i'], beta)

            # 下個 beta 階段從本次最理想的解出發
            x = best_x.copy()
            
            #mapped_x = self.mapping(x, self.config_dict['eta_i'], beta)
            #ff_fields, near_fields = self._get_near_fields_and_farfields(mapped_x)

            
            if mp.am_master() and (mapped_x is not None):

                # 只有 Master 核心繪圖前才進行 2D 變形，防止手性圖因為 1D 陣列而噴錯
                if ff_fields is not None:
                    ff_res = self.config_dict['ff_res']
                    ff_fields = {k: v.reshape(ff_res, ff_res) for k, v in ff_fields.items()}
                    
                # 1. 存結構數據
                utils.save_structure_data(self.cfg.dir_path, best_iter, beta, best_x)

                # 2. 結構圖
                utils.plot_design(
                    plot_sim=self.plot_sim,
                    design_variables=self.design_var,
                    mapped_x=mapped_x,
                    Nx=self.Nx,
                    Ny=self.Ny,
                    iters=best_iter,
                    beta=beta,
                    dir_path=self.cfg.dir_path,
                    design_center=self.design_center,
                    design_size=self.design_size,
                    opt_problem=self.opt_problem
                )
                print(f'plot_design done. iters={best_iter}')
                
                # 3. 近場相位圖（數據已由所有 rank 取出，這裡只畫圖）
                utils.plot_phase_analysis(
                    near_fields=near_fields,
                    iter_num=best_iter,
                    beta=beta,
                    dir_path=self.cfg.dir_path,
                    design_size=self.design_size,
                )
                print(f'plot_phase_analysis done. iters={best_iter}')
                

                utils.plot_near_chirality(
                        near_fields=near_fields,
                        iter_num=best_iter,
                        beta=beta,
                        dir_path=self.cfg.dir_path,
                        cfg=self.config_dict
                    )
                print(f'plot_near_chirality done. iters={best_iter}')
                
                    # 4. 遠場圖
                utils.plot_farfield_analysis(
                    ff_fields=ff_fields,
                    iter_num=best_iter,
                    beta=beta,
                    dir_path=self.cfg.dir_path,
                    cfg=self.config_dict
                )
                print(f'plot_farfield_analysis done. iters={best_iter}')
                
                # 遠場手性密度圖
                utils.plot_ff_chirality(
                    ff_fields=ff_fields,
                    iter_num=best_iter,
                    beta=beta,
                    dir_path=self.cfg.dir_path,
                    cfg=self.config_dict
                )
                print(f'plot_ff_chirality done. iters={best_iter}')
                # 空間手性傳播圖（ASM 角譜法）
                if near_fields is not None:
                    utils.plot_chirality_propagation(
                        near_fields=near_fields,
                        iter_num=best_iter,
                        beta=beta,
                        dir_path=self.cfg.dir_path,
                        cfg=self.config_dict,
                        n_slices=2
                    )
                    
                winding = utils.plot_phase_winding(
                    ff_fields=ff_fields,
                    iter_num=best_iter,
                    beta=beta,
                    dir_path=self.cfg.dir_path,
                    cfg=self.config_dict,                  # 移除 design_size=self.design_size
                    l_charge=self.config_dict['l_charge'],
                    r_fraction=None                        # 建議改為 None，讓程式自動精準追蹤遠場強度峰值 (50.61%)
                )
                print(f'Far-Field Phase winding(LCP) = {winding:.3f} × 2π (expected = {self.config_dict["l_charge"]})')
                
                print(f"Beta {beta} finished. Best FoM: {snap['fom']:.6f} when iter = {best_iter}")

        if mp.am_master():
            print("\nOptimization Finished.")
            utils.save_npy(self.cfg.dir_path, "final_purity_history.npy",
                           np.array(self.history_purity))
            utils.plot_purity_history(self.history_purity, self.beta_checkpoints,
                                      self.cfg.dir_path)
            
            utils.save_npy(self.cfg.dir_path, "final_overlap_abs2_history.npy",
                           np.array(self.history_overlap))
            utils.plot_overlap_history(self.history_overlap, self.beta_checkpoints,
                                      self.cfg.dir_path)
            
            utils.save_npy(self.cfg.dir_path, "final_FoM_history.npy",
                           np.array(self.history_FOM))
            utils.plot_FOM_history(self.history_FOM, self.beta_checkpoints,
                                      self.cfg.dir_path)