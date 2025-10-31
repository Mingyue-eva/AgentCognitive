Accessing chunks on zarr backed xarray seems to load entire array into memory

### What happened?

I opened a dataset stored as a Zarr archive on a remote server by giving xarray the URL and specifying the “zarr” engine. Although the dataset object remained lazy, asking for its `chunks` property caused xarray to begin reading array data from the remote store. In the process of inspecting chunk sizes, every chunk was fetched into memory, so the entire dataset was downloaded and loaded rather than just its metadata.

### What did you expect to happen?

According to @rabernat accessing the chunks attribute should simply inspect the `encoding` attribute on the underlying DataArrays.

### Minimal Complete Verifiable Example

_No response_

### Relevant log output

When retrieving the chunk information, xarray triggered a series of low-level getitem calls that streamed data for all chunks from the remote Zarr store. This operation blocked indefinitely while fetching the data, and I ultimately had to cancel it with a keyboard interrupt.

### Anything else we need to know?

_No response_

### Environment

<details>
INSTALLED VERSIONS
------------------
commit: None
python: 3.9.12 | packaged by conda-forge | (main, Mar 24 2022, 23:24:38)
[Clang 12.0.1 ]
python-bits: 64
OS: Darwin
OS-release: 21.2.0
machine: arm64
processor: arm
byteorder: little
LC_ALL: None
LANG: en_US.UTF-8
LOCALE: ('en_US', 'UTF-8')
libhdf5: None
libnetcdf: None

xarray: 2022.3.0
pandas: 1.4.2
numpy: 1.21.2
scipy: 1.8.0
netCDF4: None
pydap: None
h5netcdf: None
h5py: None
Nio: None
zarr: 2.8.1
cftime: None
nc_time_axis: None
PseudoNetCDF: None
rasterio: None
cfgrib: None
iris: None
bottleneck: 1.3.4
dask: 2022.04.0
distributed: 2022.4.0
matplotlib: 3.4.3
cartopy: None
seaborn: None
numbagg: None
fsspec: 2022.3.0
cupy: None
pint: None
sparse: None
setuptools: 62.0.0
pip: 22.0.4
conda: None
pytest: 7.1.1
IPython: 8.2.0
sphinx: None
</details>