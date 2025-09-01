import xarray as xr

# Load model restart file (NetCDF format)
restart_path = "ufs_restart.nc"
ds = xr.open_dataset(restart_path)

# Example: extract soil moisture variable
soil_moisture = ds['soil_moisture']  # shape: [layer, lat, lon]

# Load or define analysis increment (same shape as soil_moisture)
# This could come from an external DA system like JEDI
analysis_increment = xr.open_dataarray("sm_increment.nc")

# Apply increment
soil_moisture_updated = soil_moisture + analysis_increment

# Clip to physical bounds (e.g., 0–1 for volumetric SM)
soil_moisture_updated = soil_moisture_updated.clip(min=0.0, max=1.0)

def enforce_water_balance(sm, precip, et, runoff, drainage):
    net_input = precip - et - runoff - drainage
    sm_total = sm.sum(dim='layer')
    correction = net_input - sm_total
    sm_corrected = sm + correction / sm.sizes['layer']
    return sm_corrected.clip(min=0.0, max=1.0)

# Example usage (assuming fluxes are available in ds)
sm_balanced = enforce_water_balance(
    soil_moisture_updated,
    ds['precip'],
    ds['evapotranspiration'],
    ds['runoff'],
    ds['drainage']
)

# Replace old soil moisture with updated values
ds['soil_moisture'][:] = sm_balanced

# Save to new restart file
ds.to_netcdf("ufs_restart_updated.nc")
