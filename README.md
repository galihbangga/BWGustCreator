# BWGustCreator

BWGustCreator generates wind files in the DNV Bladed binary `.wnd` format. It is intended for creating deterministic wind-field test cases with a prescribed gust in wind speed and, optionally, a changing wind direction.

The project currently provides two gust layouts:

- **1D gust**: the same speed and direction time series is applied uniformly over the whole Y-Z grid plane.
- **2D gust**: a localized radial gust is applied over the Y-Z plane using a tanh-shaped spatial profile. The gust center and spatial extent can be configured.

Both layouts generate the velocity components `vx`, `vy`, and `vz`, as well as wind-speed and wind-direction arrays. Diagnostic time-series plots and 2D contour plots are also written for each run.

> This software is provided without guarantee. Validate generated wind files before using them in production simulations.

## Gust Shapes

The implemented gust shapes are:

- `HALF`: rises to the specified amplitude and remains at the elevated level after the end time.
- `IEC`: IEC extreme operating gust shape that returns to the baseline after the gust interval.

`FULL` is not currently implemented in `gust_creator.py`, despite being mentioned in an older error message.

## Requirements

- Python 3
- NumPy
- Matplotlib

Install the Python dependencies with:

```bash
pip install numpy matplotlib
```

## Running the Example

The example inputs and execution flow are in [`main.py`](main.py). Edit the active parameter block, then run:

```bash
python main.py
```

The active example creates a localized 2D gust. The commented sections in `main.py` contain example setups for a 1D gust and a coherent 2D gust.

The code prepares an output directory, generates diagnostic figures and a log file, and writes the requested `.wnd` file. Existing output folders in this repository include [`Output`](Output), [`Output_Coherent`](Output_Coherent), and [`Output_InCoherent`](Output_InCoherent).

## 1D Gust Inputs

The 1D workflow is called through `manager.create_gust_1D()` and uses these inputs:

| Parameter | Description |
| --- | --- |
| `TimeEnd` | Duration of the primary wind signal in seconds. |
| `TimeStep` | Wind-file time step in seconds. |
| `TimeSmooth` | Additional linear ramp duration used to return the velocity to its initial value. |
| `GustTypeSpeed` | Speed gust shape: `HALF` or `IEC`. |
| `GustSpeedStartTime` | Speed gust start time in seconds. |
| `GustSpeedEndTime` | Speed gust end time in seconds. |
| `GustSpeedStart` | Baseline wind speed in m/s. |
| `GustSpeedAmplitude` | Speed gust amplitude in m/s. |
| `GustTypeDir` | Direction gust shape: `HALF` or `IEC`. |
| `GustDirStartTime` | Direction gust start time in seconds. |
| `GustDirEndTime` | Direction gust end time in seconds. |
| `GustDirStart` | Baseline wind direction in degrees. |
| `GustDirAmplitude` | Direction gust amplitude in degrees. |
| `Ly`, `Lz` | Lateral and vertical grid dimensions in metres. |
| `dy`, `dz` | Lateral and vertical grid spacing in metres. |

## 2D Gust Inputs

The 2D workflow is called through `manager.create_gust_2D()`. It uses the same direction inputs as the 1D workflow, plus:

| Parameter | Description |
| --- | --- |
| `Gust2DSpeedStartTime` | Time at which the localized gust reaches full magnitude. |
| `Gust2DSpeedEndTime` | Time at which the localized gust starts to decay. |
| `Gust2DSpeedStart` | Uniform baseline wind speed in m/s. |
| `Gust2DEccentricity` | Inverse spatial scale of the radial gust. Larger values produce a smaller, sharper gust core. |
| `GustCenter_Y` | Gust-center offset from the grid center in the lateral direction, in metres. |
| `GustCenter_Z` | Gust-center offset from the grid center in the vertical direction, in metres. |
| `HubHeight` | Hub height used to convert the vertical grid to absolute height. |
| `NominalRotorDiameter` | Un-coned rotor diameter used for the reference circle in contour plots. |

For the 2D gust, `TimeSmooth` controls the linear rise and fall around the speed-gust interval and must be smaller than `Gust2DSpeedStartTime`.

## Wind-File Metadata

These parameters are passed to `manager.generate_wind_file()` and describe the turbine and simulation setup:

| Parameter | Description |
| --- | --- |
| `TowerExtremaLocation` | Largest absolute support-structure coordinate in metres; relevant for jacket or large support structures. |
| `NominalRotorDiameter` | Un-coned rotor diameter in metres. |
| `Overhang` | Rotor overhang in metres. |
| `LateralOffset` | Rotor lateral offset in metres. |
| `Floating` | Use `"YES"` or `"NO"` for floating-turbine metadata. |
| `SeaDepth` | Sea depth in metres; relevant for floating configurations. |
| `InitialNacelleAngle` | Initial nacelle angle in degrees. |
| `RotorOrientation` | `"UPWIND"` or `"DOWNWIND"`. |
| `OriginOfWindFileStart` | Wind-file reference origin, currently `"HUB"` or `"GLOBAL"`. |
| `OutName` | Output filename with the `.wnd` extension, for example `Wind_2DGust.wnd`. |

## Generated Files

Depending on the selected workflow, the output directory contains:

- The generated Bladed wind file (`.wnd`).
- `WindFileCreatorLog.dat`, containing grid, turbine, and gust parameters.
- Three wind-signal plots at representative grid locations.
- For 2D gusts, start, midpoint, and end contour plots for `vx` and `vy` using a consistent color scale.

## Project Layout

| Path | Purpose |
| --- | --- |
| [`main.py`](main.py) | Example inputs and executable workflow. |
| [`BladedWindCreator/gust_creator.py`](BladedWindCreator/gust_creator.py) | Gust generation and spatial expansion. |
| [`BladedWindCreator/manager.py`](BladedWindCreator/manager.py) | Public workflow wrappers and wind-file orchestration. |
| [`BladedWindCreator/plotter.py`](BladedWindCreator/plotter.py) | Diagnostic signal and contour plots. |
| [`BladedWindCreator/wind_file_creator.py`](BladedWindCreator/wind_file_creator.py) | Bladed wind-grid and binary file creation. |

## Contributing and Bugs

Contributions are welcome. For bugs or questions, contact Galih Bangga at [galih.bangga@dnv.com](mailto:galih.bangga@dnv.com).
