import sys; from ov import fetch
bb=(16.70,39.74,18.62,41.24)
jobs=[('places','place'),('addresses','address'),('base','water'),('base','land_use'),('base','land'),('transportation','segment'),('divisions','division_area'),('divisions','division')]
for theme,typ in jobs:
    fetch(theme,typ,f'puglia/{typ}.parquet',bbox=bb)
