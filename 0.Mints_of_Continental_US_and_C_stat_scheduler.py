# Mints of the Continental United States and Canada 
# Scheduler for daily stat collection from iNaturalist
# This script focuses on collecting data on which ranks of Lamiaceae need the most attention from curators on iNat.
# Daily stat collection will allow for an evaluation of progress made by indentifiers working on mints. 
# Scheduling was done through a crond.  You'll need to change this for your own server, but this is how I did it:
# 59 19 * * * source /etc/profile.d/modules.sh ; module load python/3.8 ; python /blue/soltis/aabair/iNaturalist_monitoring/0.Mints_of_Continental_US_and_C_stat_scheduler.py>> /blue/soltis/aabair/iNaturalist_monitoring/crond_error.log 2>&1

# Importing packages
import os
import urllib.request, urllib.parse, urllib.error
import json
import csv
import pandas as pd
from datetime import date

#You'll need to create you're own directory and navigate to it.
os.chdir("/iNaturalist_monitoring")

# Initializing the table with column headers.  Only run once, then comment out.
mint_stats_init = open("./mint_stats.txt", "w+")
mint_stats_header = ("Date,Family,Subfamily,(Sub)Tribe,Genus,<Subgenus,Total_Needs_ID,Total_Research_Grade,Total_Observations,Casual_in_Project_Area" + "\n")
mint_stats_init.write(mint_stats_header)
mint_stats_init.close()

# Define the service URL string to be used for each JSON request
serviceurl = 'https://api.inaturalist.org/v1/observations?project_id=mints-of-the-continental-us-and-canada&'

# Define URL strings for each Lamiaceae rank category of interest
family_url = serviceurl + urllib.parse.urlencode({"hrank":"family"}) + "&" + urllib.parse.urlencode({"lrank":"family"}) + "&" + urllib.parse.urlencode({"quality_grade":"needs_id"})
subfamily_url = serviceurl + urllib.parse.urlencode({"hrank":"subfamily"}) + "&" + urllib.parse.urlencode({"lrank":"subfamily"}) + "&" + urllib.parse.urlencode({"quality_grade":"needs_id"})
tribe_url = serviceurl + urllib.parse.urlencode({"hrank":"tribe"}) + "&" + urllib.parse.urlencode({"lrank":"subtribe"}) + "&" + urllib.parse.urlencode({"quality_grade":"needs_id"})
genus_url = serviceurl + urllib.parse.urlencode({"hrank":"genus"}) + "&" + urllib.parse.urlencode({"lrank":"genus"}) + "&" + urllib.parse.urlencode({"quality_grade":"needs_id"})
species_url = serviceurl + urllib.parse.urlencode({"hrank":"subgenus"}) + "&" + urllib.parse.urlencode({"quality_grade":"needs_id"})
total_need_id_url = serviceurl + urllib.parse.urlencode({"quality_grade":"needs_id"})
total_rg_url = serviceurl + urllib.parse.urlencode({"quality_grade":"research"})
total_obs_url = serviceurl + urllib.parse.urlencode({"quality_grade":"any"})
casual_url = "https://api.inaturalist.org/v1/observations?" + urllib.parse.urlencode({"quality_grade":"casual"}) + "&" + urllib.parse.urlencode({"not_in_place":"11"}) + "&" + urllib.parse.urlencode({"place_id":"6712,1"}) + "&" + urllib.parse.urlencode({"taxon_id":"48623"}) + "&" + urllib.parse.urlencode({"verifiable":"any"})

# Initialize a row for today's date
date_line = str(date.today())

# Extract observarion numbers from each Lamiaceae rank subset
for url in [family_url, subfamily_url, tribe_url, genus_url, species_url, total_need_id_url, total_rg_url, total_obs_url, casual_url]:
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    js = json.loads(data)
    date_line = (date_line + "," + str(js["total_results"]).replace("'", ""))

# Write mint stats to a text file 
mint_stats = open(r"./mint_stats.txt","a")
mint_stats.write(date_line + "\n")
mint_stats.close()

# Write mint stats to a backup folder with CSV files made every day
mint_stats_df = pd.read_csv('./mint_stats.txt')
mint_stats_df.to_csv(("./mint_stats_" + str(date.today()) + ".csv"), index=False)
