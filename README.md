# BIOS-SCOPE 2026 Cruise Context

Environmental-context maps and supporting station metadata for BIOS-SCOPE cruise AE2624 aboard the R/V *Atlantic Explorer* (October 2026).

The initial workflow is patterned after the SPARC 2025 cruise-context repository and is set up to generate NASA PACE OCI chlorophyll maps with the BIOS-SCOPE stations overlaid.

## Map extents

PACE/Earthaccess bounding boxes use `(west, south, east, north)`:

- **Detailed station map:** `(-64.80, 31.00, -63.40, 32.35)`
- **Regional context map:** `(-65.00, 30.00, -62.00, 33.00)`

The workflow requests the 4 km PACE product, matching the SPARC notebook and providing substantially finer source pixels than the 0.1° product.

## Station locations

The source of truth is [`data/station_locations.csv`](data/station_locations.csv). Hydrostation S and Stations 3, 11, and 13 are from Venter et al. (2004), supporting Table S1. West longitudes are negative.

| Station | Latitude | Longitude 
|---|---:|---:|---|
| BATS | 31.833333 | -64.166667 
| Hydrostation S | 32.166667 | -64.500000 
| Station 13 | 31.535000 | -63.595000 
| Station 11 | 31.175000 | -64.324333 
| Station 3 | 32.158500 | -64.010167 
| Station 1 | 31.750000 | -64.650000 


## Quick start

1. Create a Python environment and install the packages in `requirements.txt`.
2. Authenticate Earthdata when prompted by `earthaccess`.
3. Run:

```bash
python scripts/pace_chl_context.py --extent detail --days 8
```

For the larger historical-grid view:

```bash
python scripts/pace_chl_context.py --extent regional --days 8
```

Outputs are written beneath `figs/satellite_composites_YYYYMMDD/` as a high-resolution PNG and PDF. The PDF preserves vector labels and station symbols while the satellite raster remains at its native resolution.

From a Jupyter notebook opened at the repository root, the same command can be run in a cell:

```python
%run scripts/pace_chl_context.py --extent detail --days 8 --dpi 400
```

## Repository layout

- `config/map_config.json` - cruise dates and named bounding boxes
- `data/station_locations.csv` - station coordinates and provenance
- `notebooks/BIOSSCOPE_AE2624_PACE_CHL_Last8Days.ipynb` - notebook workflow for PACE composites and change maps
- `scripts/BIOSSCOPE_AE2624_argoFloats_context.Rmd` - BGC-Argo track, profile, and Hovmöller workflow
- `scripts/pace_chl_context.py` - PACE rolling-median map workflow
- `scripts/update_fig_index.R` - refreshes archive links and latest previews
- `figs/` - generated figure archives and latest products

Raw downloaded Argo NetCDF files are kept locally under `data/argo/` and excluded from Git. Generated context figures are intentionally tracked so they can be viewed directly on GitHub, matching the SPARC repository workflow.

## Coordinate conventions

- Decimal degrees use positive north and negative west.
- Degrees-minutes conversion is `decimal = degrees + minutes / 60`, with a negative sign applied to west longitude.
- Do not silently normalize or replace coordinates: update the CSV status/source columns at the same time.

<!-- BIOSSCOPE_CONTEXT_PREVIEWS -->

### Latest previews

**PACE satellite context**

![](figs/latest/satellite/PACE_CHL_last8d_median_20260830.png)

**BGC-Argo float context**

![](figs/latest/float/Float_6999997_20260831.png)

<!-- BIOSSCOPE_CONTEXT_PREVIEWS -->
