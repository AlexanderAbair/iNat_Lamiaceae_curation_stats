#!/usr/bin/bash
# The CSV files produced by my python script produce a decimal in the value of the last column.
# I think Pandas is converting a string to a float in the dataframe for some reason.
# This script removes the decimals after the CSV files have been created.
# Just run it at any time to clean all files in the "backup_CSV_stats" folder

sed -i 's/\.0//' *.csv

# Why not get rid of the crond_error.log file while I'm at it...

rm crond_error.log
