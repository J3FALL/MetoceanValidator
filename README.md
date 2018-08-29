# nemo-error-checker

A tool for finding errors in ocean simulation results by NEMO model.

[![Build Status](https://travis-ci.com/J3FALL/nemo-error-checker.svg?branch=master)](https://travis-ci.com/J3FALL/nemo-error-checker)

This tool is considered to be a part of Metocean Simulation Results Verification Framework. 
The experiments are based mainly on ocean simulation results obtained with NEMO model.

The tool focuses on technical verification of simulation results, such as:
- Search for some missing resulted files
- Search for some for fully-corrupted files or with incorrect meta-data
- Check for the presence of all oceanic variables
- Check that variables do not contain invalid values, such as `nan` or `inf`
- Some others (probably will be designed later)

The simulation results are stored in NetCDF format which allows you to effectively handle multidimensional data arrays.

To work with NetCDF a Python library [netcdf4-python by Unidata](https://github.com/Unidata/netcdf4-python) is used that provides a good interface for NetCDF [C library](https://github.com/Unidata/netcdf-c).
