# BWGustCreator

BWGustCreator generates wind files in the DNV Bladed binary `.wnd` format. It is intended for creating deterministic wind-field test cases with a prescribed gust in wind speed and, optionally, a changing wind direction.

The project currently provides three gust layouts:

- **1D gust**: the same speed and direction time series is applied uniformly over the whole Y-Z grid plane.
- **2D circular gust**: a localized circular gust is applied over the Y-Z plane. The time evolution follows the `HALF`, `FULL`, or `IEC` shape and the spatial profile is smoothed at the gust edge. The gust radius and center can be configured.
- **2D IEA Wind Task 47 gust**: a localized radial gust is applied over the Y-Z plane using a tanh-shaped spatial profile and a trapezoidal time evolution. The gust center and spatial extent can be configured.

All layouts generate the velocity components `vx`, `vy`, and `vz`, as well as wind-speed and wind-direction arrays. Diagnostic time-series plots and 2D contour plots are also written for each run.

> This software is provided without guarantee. Validate generated wind files before using them in production simulations.

## Gust Shapes

The implemented gust shapes are:

- `HALF`: rises to the specified amplitude and remains at the elevated level after the end time.
- `FULL`: rises to the specified amplitude and returns to the baseline at the end time.
- `IEC`: IEC extreme operating gust shape that returns to the baseline after the gust interval.

## Requirements

- Python 3
- NumPy
- Matplotlib

Install the Python dependencies with:

```bash
pip install numpy matplotlib
```

## Running the Example

The example inputs and execution flow are in [`main.py`](main.py). Edit the parameter block of one example, then run:

```bash
python main.py
```

The active example creates a circular 2D gust. The commented sections in `main.py` contain example setups for a 1D gust and for coherent and incoherent IEA Wind Task 47 2D gusts; uncomment one block (and comment out the active one) to run it. The code prepares an output directory, generates diagnostic figures and a log file, and writes the requested `.wnd` file.

## 1D Gust Inputs

The 1D workflow is called through `manager.create_gust_1D()` and uses these inputs:

| Parameter | Description |
| --- | --- |
| `TimeEnd` | Duration of the primary wind signal in seconds. |
| `TimeStep` | Wind-file time step in seconds. |
| `TimeSmooth` | Duration at the end of the wind file replaced by a linear ramp back to the initial value. |
| `GustTypeSpeed` | Speed gust shape: `HALF`, `FULL`, or `IEC`. |
| `GustSpeedStartTime` | Speed gust start time in seconds. |
| `GustSpeedEndTime` | Speed gust end time in seconds. |
| `GustSpeedStart` | Baseline wind speed in m/s. |
| `GustSpeedAmplitude` | Speed gust amplitude in m/s. |
| `GustTypeDir` | Direction gust shape: `HALF`, `FULL`, or `IEC`. |
| `GustDirStartTime` | Direction gust start time in seconds. |
| `GustDirEndTime` | Direction gust end time in seconds. |
| `GustDirStart` | Baseline wind direction in degrees. |
| `GustDirAmplitude` | Direction gust amplitude in degrees. |
| `Ly`, `Lz` | Lateral and vertical grid dimensions in meters. |
| `dy`, `dz` | Lateral and vertical grid spacing in meters. |

## 2D Circular Gust Inputs

The circular 2D workflow is called through `manager.create_gust_2D_circular()`. The gust follows the `HALF`, `FULL`, or `IEC` shape in time and a smoothed radial shape in space, defined by the gust radius. It uses all 1D inputs, where `GustSpeedAmplitude` is the amplitude at the gust center, plus:

| Parameter | Description |
| --- | --- |
| `GustRadius` | Gust radius in meters. The gust amplitude is halved at this distance from the gust center and decays smoothly to zero around it. |
| `GustCenter_Y` | Gust-center offset from the grid center in the lateral direction, in meters. |
| `GustCenter_Z` | Gust-center offset from the grid center in the vertical direction, in meters. |
| `HubHeight` | Hub height used to convert the vertical grid to absolute height. |
| `NominalRotorDiameter` | Un-coned rotor diameter used for the reference circle in contour plots. |

The wind direction gust is applied uniformly over the grid, while the speed gust amplitude is scaled in space by the smoothed radial profile.

## 2D IEA Wind Task 47 Gust Inputs

The IEA Wind Task 47 workflow is called through `manager.create_gust_2D_IEAWind47()`. It uses the 1D inputs `TimeEnd`, `TimeStep`, the direction gust inputs, and the grid inputs. `TimeSmooth` is redefined and the speed gust is defined by the following inputs instead of the 1D speed gust inputs:

| Parameter | Description |
| --- | --- |
| `TimeSmooth` | Duration of the linear rise before `Gust2DSpeedStartTime` and of the linear fall after `Gust2DSpeedEndTime` of the speed gust. It is also the duration at the end of the wind file replaced by a linear ramp back to the initial value. Must be smaller than `Gust2DSpeedStartTime`. |
| `Gust2DSpeedStartTime` | Time at which the localized gust reaches full magnitude. |
| `Gust2DSpeedEndTime` | Time at which the localized gust starts to decay. |
| `Gust2DSpeedStart` | Uniform baseline wind speed in m/s. |
| `Gust2DEccentricity` | Inverse spatial scale of the radial gust. Larger values produce a smaller, sharper gust core. |
| `GustCenter_Y` | Gust-center offset from the grid center in the lateral direction, in meters. |
| `GustCenter_Z` | Gust-center offset from the grid center in the vertical direction, in meters. |
| `HubHeight` | Hub height used to convert the vertical grid to absolute height. |
| `NominalRotorDiameter` | Un-coned rotor diameter used for the reference circle in contour plots. |


## Wind-File Metadata

These parameters are passed to `manager.generate_wind_file()` and describe the turbine and simulation setup:

| Parameter | Description |
| --- | --- |
| `TowerExtremaLocation` | Largest absolute support-structure coordinate in meters; relevant for jacket or large support structures. |
| `NominalRotorDiameter` | Un-coned rotor diameter in meters. |
| `Overhang` | Rotor overhang in meters. |
| `LateralOffset` | Rotor lateral offset in meters. |
| `Floating` | Use `"YES"` or `"NO"` for floating-turbine metadata. |
| `SeaDepth` | Sea depth in meters; relevant for floating configurations. |
| `InitialNacelleAngle` | Initial nacelle angle in degrees. |
| `RotorOrientation` | `"UPWIND"` or `"DOWNWIND"`. |
| `OriginOfWindFileStart` | Wind-file reference origin, currently `"HUB"` or `"GLOBAL"`. |
| `OutName` | Output filename with the `.wnd` extension, for example `Wind_2DGust.wnd`. |

## Generated Files

Depending on the selected workflow, the output directory contains:

- The generated Bladed wind file (`.wnd`).
- `WindFileCreatorLog.dat`, containing grid, turbine, and gust parameters.
- Three wind-signal plots at representative grid locations.
- For 2D gusts, start, quarter, midpoint, three-quarter, and end contour plots for `vx` and `vy` using a consistent color scale.
- For 2D gusts, `Wind_Profile_Z.png` and `Wind_Profile_Y.png` with the vertical and lateral profiles of `vx` and `vy` at the same five time instances, taken through the turbine center (`y = 0` and hub height).

## Contributing and Bugs

Contributions are welcome. For bugs or questions, contact Galih Bangga at [galih.bangga@dnv.com](mailto:galih.bangga@dnv.com).
