# MetoceanValidator

A tool for errors detection in hydrometeorological simulation results obtained with different metocean models.

[![Build Status](https://travis-ci.com/J3FALL/MetoceanValidator.svg?branch=master)](https://travis-ci.com/J3FALL/MetoceanValidator)

This tool is considered to be a part of Metocean Simulation Results Validation Framework. 
The experiments are based mainly on simulation results obtained with 3 models:
- NEMO (ocean model)+ LIM3 module (ice model): Ice aggregation and dynamics, tracers (sea surface height, temperature, salinity), currents
- WRF (atmosphere model): pressure, temperature, directions
- WaveWatch III (ocean wave model): significant height of wind and swell, mean direction and frequency, directions

The tool focuses on technical validation of simulation results, such as:
- Search for some missing resulted files
- Search for some for fully-corrupted files or with incorrect meta-data
- Check for the presence of all variables
- Check that variables correspond to correct dimensions
- Check that variables do not contain invalid values, such as `nan` or `inf`

The simulation results are stored in NetCDF format which allows you to effectively handle multidimensional data arrays.

To work with NetCDF a Python library [netcdf4-python by Unidata](https://github.com/Unidata/netcdf4-python) is used that provides a good interface for NetCDF [C library](https://github.com/Unidata/netcdf-c).
