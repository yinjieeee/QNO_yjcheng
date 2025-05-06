Extraordinary Optical Transmission (EOT) is a fascinating phenomenon in nanophotonics where light is transmitted through **subwavelength** apertures in opaque metal films with efficiencies far exceeding classical predictions. Discovered in the late 1990s, EOT has opened new avenues in optics, plasmonics, and nanotechnology, enabling applications in sensing, spectroscopy, and photonic devices.

### What is EOT?

EOT refers to the enhanced transmission of light through periodic arrays of subwavelength holes or slits in metal films, such as gold or silver. According to classical aperture theory (e.g., Bethe's theory), the transmission of light through holes much smaller than the wavelength should be negligible due to diffraction limits. However, experiments have shown that when these holes are arranged in a periodic lattice, **the transmission can be orders of magnitude higher than expected**. This enhancement is primarily attributed to the excitation of surface plasmon polaritons (SPPs)—collective oscillations of electrons at the metal-dielectric interface—which couple incident light to the periodic structure.
>雖然傳統理論(eg. Bethe)認為小孔無法有效透光，但當這些小孔以特定週期排列在金屬膜上時，**透過SPPs的共振效應，光的傳輸會被大幅強化**。這就是 EOT 的核心機制，也成為許多奈米光學應用（如超解析度成像、光子晶體元件、感測器設計）的基礎

### Historical Context and Significance

The phenomenon was first experimentally demonstrated by T.W. Ebbesen and colleagues in 1998, who observed anomalously high transmission through arrays of nanoholes in a metal film. This groundbreaking work, published in _Nature_, challenged conventional understanding and sparked intense research into plasmonics and metamaterials. EOT is significant because it **bridges the gap between classical optics and quantum phenomena**, offering insights into light-matter interactions at nanoscale dimensions.

### Applications of EOT

EOT has found applications in various fields, including:

- **Biosensing**: Highly sensitive detection of biomolecules using surface plasmon resonance.
- **Photodetectors and Filters**: Enhanced light manipulation for optical devices.
- - **Nanophotonics**: Development of subwavelength optical components.
- **Spectroscopy**: Improved signal detection in Raman and infrared spectroscopy.

This notebook will guide you through the theoretical foundations, experimental techniques, and numerical simulations of EOT, providing hands-on examples to deepen your understanding of this remarkable phenomenon.

### Reference Papers

Below are some key papers for further reading:

1. Ebbesen, T.W., Lezec, H.J., Ghaemi, H.F., Thio, T., & Wolff, P.A. (1998). "Extraordinary optical transmission through sub-wavelength hole arrays." _Nature_, 391(6668), 667-669. DOI:10.1038/35570
    - The seminal paper that introduced EOT to the scientific community.

2. Garcia-Vidal, F.J., Martin-Moreno, L., Ebbesen, T.W., & Kuipers, L. (2010). "Light passing through subwavelength apertures." _Reviews of Modern Physics_, 82(1), 729-787. DOI:10.1103/RevModPhys.82.729
    - A comprehensive review of the physics behind EOT and its applications.

3. Genet, C., & Ebbesen, T.W. (2007). "Light in tiny holes." _Nature_, 445(7123), 39-46. DOI:10.1038/nature05350
    - Discusses the role of surface plasmons and the potential of EOT in nanotechnology.

4. Pendry, J.B., Martin-Moreno, L., & Garcia-Vidal, F.J. (2004). "Mimicking surface plasmons with structured surfaces." _Science_, 305(5685), 847-848. DOI:10.1126/science.1098999
    - Explores theoretical aspects of plasmonic structures related to EOT.


These references provide a solid foundation for understanding EOT and can serve as a starting point for deeper exploration.

---

## Python
### 環境設定

```python
import meep as mp
import numpy as np
from meep.materials import Al, Ag
from meep_plot_style import * #把 `meep_plot_style` 模組裡**所有的公開成員**都匯入到目前這個程式的命名空間
import h5py #h5py → numpy → pyplot
import os
```

### 參數設定
```python
# Define simulation parameters
a = 0.5           # Unit length, corresponds to 1 micron
h = 0.2    # Film thickness, 20 nm in simulation units (a = 600 nm)
r = 0.1   # Hole radius, 100 nm in simulation units
dpml = 0.5        # PML thickness
sz = 1.5          # Cell size in z-direction (non-PML region from z=-2 to z=2)
cell_size = mp.Vector3(a, a, sz)
resolution = 100  # Pixels per unit length (600 nm / 100 = 6 nm per pixel)
fcen = 1 / 0.6      # Center frequency, f = c/lambda, lambda = 600 nm = a, so f = c/a = 1
df = 1          # Frequency width for the Gaussian pulse
nfreq = 100     # Number of frequency points for the spectrum

# Define the geometry: silver film with a circular hole
geometry = [
    # Silver film as a block, infinite in x and y due to periodic boundaries
    mp.Block(
        size=mp.Vector3(mp.inf, mp.inf, h),
        center=mp.Vector3(0, 0, 0),
        material=Ag  # Predefined silver material in Meep
    ),
    # Circular hole as a cylinder of air through the film
    mp.Cylinder(
        radius=r,
        height=h,
        center=mp.Vector3(0, 0, 0),
        material=mp.Medium(epsilon=1)  # Air
    )
]
```

### 波源設定
```python
# Define the source: a Gaussian pulse plane wave
sources = [
    mp.Source(
        mp.GaussianSource(frequency=fcen, fwidth=df),
        component=mp.Ex,  # x-polarized electric field
        center=mp.Vector3(0, 0, -0.2),  # Positioned before the film
        size=mp.Vector3(a, a, 0)  # Spans the xy-plane of the unit cell
    )
]

boundary_layers=[mp.Absorber(thickness=dpml, direction=mp.Z)] ## !! Here, I do not use pml since pml can not deal with wave propagating parallel to the plane
```
>!! Here, I do not use pml since pml can not deal with wave propagating parallel to the plane
### 模擬(no 結構)
```python
# sim without structure
sim = mp.Simulation(
    cell_size=cell_size,
    resolution=resolution,
    boundary_layers=boundary_layers,
    sources=sources,
    k_point=mp.Vector3(0, 0, 0),
    geometry=[]
)

# Add flux monitor for  incident
flux_inci = sim.add_flux(
    fcen,
    df,
    nfreq,
    mp.FluxRegion(
        center=mp.Vector3(0, 0, 0.2),
        size=mp.Vector3(a, a, 0)
    )
)
# Run the simulation
# Run the simulation
sim.run(until_after_sources=mp.stop_when_fields_decayed(5, mp.Ex, mp.Vector3(), 1e-6))
# Get the incident flux data
incident_flux = mp.get_fluxes(flux_inci)
```

### 繪圖(no 結構，純波源)
```python
import matplotlib
import matplotlib.pyplot as plt
output_plane_yz = mp.Volume(
        center=mp.Vector3(0, 0, 0),  # Center of the plane
        size=mp.Vector3(0, a, sz)     # Size: full x and y, zero thickness in z
    )
output_plane_xy = mp.Volume(
        center=mp.Vector3(0, 0, 0),  # Center of the plane
        size=mp.Vector3(a, a, 0)     # Size: full x and y, zero thickness in z
    )
plt.subplot(1,2,1)
sim.plot2D(fields=mp.Ex, output_plane = output_plane_xy,eps_parameters={'cmap':cmap_alpha,'vmin':-45,'alpha':0.25}
          ,field_parameters={'cmap':cmap_br,'post_process':np.real,'vmin':-1,'vmax':1})
plt.subplot(1,2,2)
sim.plot2D(fields=mp.Ex, output_plane = output_plane_yz,eps_parameters={'cmap':'gray','vmin':-45,'alpha':0.25}
           ,field_parameters={'cmap':cmap_br,'post_process':np.real,'vmin':-1,'vmax':1})
plt.show()
```

### 模擬(波源 with 結構)+穿透流(transmitted flux)
```python
# Step 2: Simulation with the structure to compute transmitted flux
sim.reset_meep()  # Reset the simulation

sim = mp.Simulation(
    cell_size=cell_size,
    resolution=resolution,
    boundary_layers=boundary_layers,
    sources=sources,
    k_point=mp.Vector3(0, 0, 0),
    geometry=geometry  # Include the film and hole
)

# Add flux monitor at the same position as in the empty simulation
flux_trans = sim.add_flux(
    fcen,
    df,
    nfreq,
    mp.FluxRegion(
        center=mp.Vector3(0, 0, 0.2),
        size=mp.Vector3(a, a, 0)
    )
)

# Run the simulation
sim.run(until_after_sources=mp.stop_when_fields_decayed(5, mp.Ex, mp.Vector3(), 1e-6))
# Get the transmitted flux data
transmitted_flux = mp.get_fluxes(flux_trans)
```

### 繪圖(波源 with 結構)
```python
output_plane_yz = mp.Volume(
        center=mp.Vector3(0, 0, 0),  # Center of the plane
        size=mp.Vector3(0, a, sz)     # Size: full x and y, zero thickness in z
    )
output_plane_xy = mp.Volume(
        center=mp.Vector3(0, 0, 0),  # Center of the plane
        size=mp.Vector3(a, a, 0)     # Size: full x and y, zero thickness in z
    )
plt.subplot(1,2,1)
sim.plot2D(fields=mp.Ex,output_plane = output_plane_xy,eps_parameters={'cmap':'Greys','vmin':-5.5,'alpha':0.9}
          ,field_parameters={'cmap':cmap_br,'post_process':np.real,'vmin':-1,'vmax':1})
plt.subplot(1,2,2)
sim.plot2D(fields=mp.Ex,output_plane = output_plane_yz,eps_parameters={'cmap':'Greys','vmin':-5.5,'alpha':0.9}
           ,field_parameters={'cmap':cmap_br,'post_process':np.real,'vmin':-1,'vmax':1})
plt.show()
```

### 計算穿透光譜
```python
# Compute the transmission spectrum
transmission = [t / i for t, i in zip(transmitted_flux, incident_flux)]

# Extract transmission at the center frequency
flux_freqs = mp.get_flux_freqs(flux_trans)
index = np.argmin(np.abs(np.array(flux_freqs) - fcen))
transmission_at_fcen = transmission[index]
```

### 繪圖(穿透光譜)
```python
# Output the result
print(f"Transmission at f = {fcen} (lambda = 600 nm): {transmission_at_fcen}")

# Optional: Plot the transmission spectrum
import matplotlib.pyplot as plt
plt.plot(1000/ np.array(flux_freqs), transmission, 'y-', label='Transmission')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Transmission')
plt.ylim([0,1])
plt.title('Transmission Spectrum of Silver Film with Hole')
plt.legend()
plt.grid(True)
plt.show()
```

### 用MEEP 模擬電磁場的動態變化(MP4)
```python
#%%capture 
# to suppress output of this cell
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np  # Assuming np is used in your post_process

# Sim duration and number of snapshots
sim_time = 15 # femtosecond
n_frames = 601 # include initial

# Simulation object
sim.reset_meep()  # Reset the simulation

sim = mp.Simulation(
    cell_size=cell_size,
    resolution=resolution,
    boundary_layers=boundary_layers,
    sources=sources,
    k_point=mp.Vector3(0, 0, 0),
    geometry=geometry  # Include the film and hole
)
```

### 繪圖
```python
# Plot
fig, (ax1, ax2) = plt.subplots(1, 2)  # Create two subplots side by side

def simulate(k):    
    # Time delta (in fs) between snapshots. Note that
    # we subtract 1 because we include the initial state
    # as the first frame.
    delta_time = sim_time / (n_frames - 1)
    elapsed = k * delta_time
    
    # Clear previous plots
    ax1.clear()
    ax2.clear()
    
    # Plot on the existing axes
    sim.plot2D(ax=ax1, output_plane=output_plane_xy, fields=mp.Ex, 
               eps_parameters={'cmap':'Greys','vmin':-5.5, 'alpha': 0.25},
               field_parameters={'cmap': cmap_br, 'post_process': np.real,'vmin':-1,'vmax':1})
    sim.plot2D(ax=ax2, output_plane=output_plane_yz, fields=mp.Ex, 
               eps_parameters={'cmap':'Greys','vmin':-5.5, 'alpha': 0.25},
               field_parameters={'cmap': cmap_br, 'post_process': np.real,'vmin':-1,'vmax':1})
    
    # Run until the next frame time
    sim.run(until=delta_time)

# Create the animation
anim = animation.FuncAnimation(fig, simulate, frames=n_frames)

# Save the animation
video_file = 'trans_ag_film.mp4'
anim.save(video_file, fps=10, extra_args=['-vcodec', 'libx264'],
          progress_callback=lambda i, n: print(i))

plt.show()
plt.close(fig)  # Close the figure to free memory
```
for `simulate`：
- 動畫用的 callback 函式，`k` 是目前是第幾幀
- `elapsed = k * delta_time`：目前時間點
- `sim.plot2D(...)`：畫場圖（例如 `Ex`），並疊加結構圖（灰色 `eps`）
    - `field_parameters` 裡的 `post_process=np.real` 表示只畫電場的**實部**
    - `cmap=cmap_br`：用你自訂的 colormap 呈現電場
- `sim.run(until=delta_time)`：從上一幀跑到這一幀的時間差

```python
from IPython.display import Video  # For displaying the video

display(Video(video_file, embed=True))
```
