# BIOS-SCOPE 2026 Cruise Context

Environmental-context maps and supporting station metadata for BIOS-SCOPE cruise AE2624 aboard the R/V *Atlantic Explorer* (October 2026).

The initial workflow is patterned after the SPARC 2025 cruise-context repository and is set up to generate NASA PACE OCI chlorophyll maps with the BIOS-SCOPE stations overlaid.

## Map extents

PACE/Earthaccess bounding boxes use `(west, south, east, north)`:

- **Detailed station map:** `(-64.80, 31.00, -63.85, 32.35)`
- **Regional context map:** `(-65.00, 30.00, -62.00, 33.00)`

The detailed box gives useful padding around all currently listed stations, including the approximate Station 1. The regional box reproduces the geographic coverage of the older BATS-grid figure and is better when mesoscale eddy context matters.

## Station locations

The source of truth is [`data/station_locations.csv`](data/station_locations.csv). West longitudes are negative.

| Station | Latitude | Longitude | Status |
|---|---:|---:|---|
| BATS | 31.833333 | -64.166667 | User-provided cruise coordinate; verify against final navigation plan |
| Hydrostation S | 32.166667 | -64.500000 | User-provided |
| Station 13 | 32.100000 | -64.095000 | Longitude normalized from invalid `63°65.70′W`; verify |
| Station 11 | 31.175000 | -64.324333 | User-provided |
| Station 3 | 32.158500 | -64.010167 | User-provided |
| Station 1 | 31.750000 | -64.650000 | Approximate from historical map; replace when authoritative coordinate is found |

Important: the supplied Venter et al. (2004) article states that exact sampling coordinates are in supporting Table S1, but that table is not included in the supplied article PDF. Station 13 and Station 1 therefore remain verification items.

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

## Repository layout

- `config/map_config.json` - cruise dates and named bounding boxes
- `data/station_locations.csv` - station coordinates and provenance
- `scripts/pace_chl_context.py` - PACE rolling-median map workflow
- `scripts/update_fig_index.R` - refreshes archive links and latest previews
- `figs/` - generated figure archives and latest products

## Coordinate conventions

- Decimal degrees use positive north and negative west.
- Degrees-minutes conversion is `decimal = degrees + minutes / 60`, with a negative sign applied to west longitude.
- Do not silently normalize or replace coordinates: update the CSV status/source columns at the same time.

<!-- BIOSSCOPE_CONTEXT_PREVIEWS -->

### Latest previews

_No figures generated yet._

<!-- BIOSSCOPE_CONTEXT_PREVIEWS -->
