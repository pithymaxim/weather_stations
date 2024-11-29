import pandas as pd
import numpy as np
import os
import requests

os.chdir(r"change this")

# Define the URL of the space-delimited file
url_inventory = "https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt"

# Define the column names
column_names = ['ID', 'LATITUDE', 'LONGITUDE', 'ELEMENT', 'FIRSTYEAR', 'LASTYEAR']

# Read the space-delimited file into a pandas DataFrame
df_inventory = pd.read_csv(url_inventory, delim_whitespace=True, header=None, names=column_names)

# Ensure LATITUDE and LONGITUDE columns are numeric
df_inventory['LATITUDE'] = pd.to_numeric(df_inventory['LATITUDE'], errors='coerce')
df_inventory['LONGITUDE'] = pd.to_numeric(df_inventory['LONGITUDE'], errors='coerce')

# Function to calculate the Haversine distance
def haversine(lon1, lat1, lon2, lat2):
    # Convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 3956 # Radius of Earth in miles. Use 6371 for kilometers.
    return c * r

# Coordinates of the specific location
target_lat, target_lon = 40.273502, -86.126976 # midpoint of Indiana

# Calculate distance for each station
df_inventory['Distance'] = haversine(df_inventory['LONGITUDE'], df_inventory['LATITUDE'], target_lon, target_lat)

# Filter stations within 400 miles, FIRSTYEAR is 2005 or earlier, and LASTYEAR is 2015 or later
final_filtered_df = df_inventory[(df_inventory['Distance'] <= 300) & (df_inventory['FIRSTYEAR'] <= 2005) & (df_inventory['LASTYEAR'] >= 2015)]

# Display the final filtered DataFrame
print(final_filtered_df)
print(f"Unique stations: {len(final_filtered_df.ID.unique())}")
print(f"Sample of unique stations: {final_filtered_df.sample(n=10).ID}")

final_filtered_df.to_stata('raw/weather/station_list.dta')

# Directory to save the downloaded .dly files
download_dir = r"change this"

# Base URL for downloading station data
base_url = "https://www.ncei.noaa.gov/pub/data/ghcn/daily/all/"

print(final_filtered_df.shape)

# Function to download a file
def download_file(station_id):
    file_url = f"{base_url}{station_id}.dly"
    response = requests.get(file_url)
    if response.status_code == 200:
        file_path = os.path.join(download_dir, f"{station_id}.dly")
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {station_id}.dly")
    else:
        print(f"Failed to download {station_id}.dly")

# Get the list of unique station IDs to download
station_ids = final_filtered_df['ID'].unique()
N = len(station_ids)

# Download the data files for each filtered station ID with counter
for i, station_id in enumerate(station_ids, 1):
    print(f"On file {i} of {N}")
    download_file(station_id)


