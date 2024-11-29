# Weather Station Data Downloader

A Python script that downloads historical weather data from NOAA's Global Historical Climatology Network (GHCN) for weather stations within a specified geographic region.

## Description

This script:
1. Downloads a complete inventory of GHCN weather stations
2. Filters stations based on:
  - Geographic proximity to Indiana (within 300 miles)
  - Data availability between 2005-2015
3. Downloads daily weather data files for all matching stations

## Requirements

- Python 3.x
- pandas
- numpy
- requests

## Key Features

- Uses Haversine formula to calculate distances between coordinates
- Filters stations by distance and date range
- Downloads .dly format weather station data files
- Saves filtered station list to Stata format
- Shows progress during download

## Usage

Set the following variables before running:
- `target_lat, target_lon`: Center coordinates for the search radius (default: Indiana's midpoint)
- `download_dir`: Directory path for saving station data files
- Distance threshold (default: 300 miles)
- Year range (default: 2005-2015)

## Data Source

Data is sourced from NOAA's GHCN daily dataset:
- Station inventory: `ghcnd-inventory.txt`
- Individual station data: `.dly` files

## Output

- Saves filtered station list as `station_list.dta`
- Downloads individual `.dly` files for each matching station to specified directory
