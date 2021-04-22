import time
import base64

import streamlit as st
import pandas as pd
import geopandas as gpd

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

locator = Nominatim(user_agent="myGeocoder")
location = locator.geocode("Champ de Mars, Paris, France")



print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))