#!/usr/bin/env python3
"""Create a rolling PACE OCI chlorophyll context map for BIOS-SCOPE AE2624."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import earthaccess
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

ROOT = Path(__file__).resolve().parents[1]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--extent", choices=("detail", "regional"), default="detail")
    p.add_argument("--days", type=int, default=8)
    p.add_argument("--end-date", help="UTC end date YYYY-MM-DD; default is yesterday")
    p.add_argument("--dpi", type=int, default=400)
    return p.parse_args()


def date_window(days, end_date=None):
    end = datetime.fromisoformat(end_date).date() if end_date else datetime.now(timezone.utc).date() - timedelta(days=1)
    start = end - timedelta(days=days - 1)
    return start.isoformat(), end.isoformat(), end.strftime("%Y%m%d")


def choose_chl(ds):
    for name in ds.data_vars:
        if "chlor" in name.lower() or name.lower() == "chl":
            return name
    raise KeyError("No chlorophyll variable found")


def subset(field, bbox):
    west, south, east, north = bbox
    lon = "lon" if "lon" in field.coords else "longitude"
    lat = "lat" if "lat" in field.coords else "latitude"
    if float(field[lon].max()) > 180:
        west, east = west % 360, east % 360
    out = field.sel({lon: slice(west, east)})
    ascending = bool(out[lat][0] < out[lat][-1])
    out = out.sel({lat: slice(south, north) if ascending else slice(north, south)})
    return out, lon, lat


def main():
    args = parse_args()
    cfg = json.loads((ROOT / "config/map_config.json").read_text())
    stations = pd.read_csv(ROOT / "data/station_locations.csv")
    bbox = cfg["bounding_boxes"][args.extent]
    start, end, tag = date_window(args.days, args.end_date)

    results = earthaccess.search_data(
        short_name=cfg["pace_short_name"],
        temporal=(start, end),
        bounding_box=tuple(bbox),
        granule_name=f"*.DAY.*.{cfg['pace_resolution_tag']}.*",
        cloud_hosted=True,
    )
    if not results:
        raise RuntimeError(f"No PACE granules found for {start} to {end}")
    paths = earthaccess.open(results[-args.days:])
    ds = xr.open_mfdataset(paths, combine="nested", concat_dim="date", engine="h5netcdf", chunks="auto")
    field = ds[choose_chl(ds)].median(dim="date", skipna=True)
    field, lon, lat = subset(field, bbox)

    finite = field.values[np.isfinite(field.values) & (field.values > 0)]
    vmin, vmax = np.nanpercentile(finite, [2, 98]) if finite.size else (0.02, 1.0)
    outdir = ROOT / "figs" / f"satellite_composites_{tag}"
    outdir.mkdir(parents=True, exist_ok=True)

    crs = ccrs.PlateCarree()
    fig, ax = plt.subplots(figsize=(8.0, 7.2), subplot_kw={"projection": crs}, constrained_layout=True)
    im = ax.pcolormesh(field[lon], field[lat], field, transform=crs, shading="auto", cmap="viridis", vmin=vmin, vmax=vmax)
    ax.set_extent(bbox, crs=crs)
    ax.add_feature(cfeature.LAND, facecolor="0.82", zorder=2)
    ax.coastlines(resolution="10m", linewidth=0.7, zorder=3)
    gl = ax.gridlines(draw_labels=True, linewidth=0.35, color="white", alpha=0.65, linestyle="--")
    gl.top_labels = False; gl.right_labels = False
    ax.xaxis.set_major_formatter(LongitudeFormatter()); ax.yaxis.set_major_formatter(LatitudeFormatter())

    for _, row in stations.iterrows():
        approx = row["coordinate_status"] in {"approximate", "verify_normalized", "verify"}
        marker = "^" if approx else "o"
        face = "none" if approx else "white"
        ax.scatter(row.longitude, row.latitude, s=52, marker=marker, facecolors=face, edgecolors="black", linewidths=1.1, transform=crs, zorder=5)
        ax.annotate(row.station, (row.longitude, row.latitude), xytext=(5, 5), textcoords="offset points", fontsize=8.5, weight="bold", color="black", transform=crs, zorder=6)

    cb = fig.colorbar(im, ax=ax, pad=0.025, shrink=0.86)
    cb.set_label("PACE OCI chlorophyll-a (mg m$^{-3}$)")
    ax.set_title(f"BIOS-SCOPE AE2624 | PACE OCI {args.days}-day median\n{start} to {end}", weight="bold")
    stem = outdir / f"PACE_CHL_{args.days}d_median_{args.extent}_{tag}"
    fig.savefig(stem.with_suffix(".png"), dpi=args.dpi, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    print(stem.with_suffix(".png"))
    print(stem.with_suffix(".pdf"))


if __name__ == "__main__":
    main()
