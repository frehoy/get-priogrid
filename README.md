#get-priogrid

IMPORTANT: This script creates a subfolder 'jsons' which reaches several GB in size after the script is done. The script does not clean this up after running but overwrites them on each run. 


Small fetcher script for data from PRIO-GRID 2 (http://grid.prio.org/).
The script downloads all the data available through the API and merges it into a single Pandas Dataframe (df_merged in the script) for further processing. 
This is done to enable automatic downloading of the the data made difficult by the use of an Angular form thingy for downloading the complete data in csv at http://grid.prio.org/#/download. 

#TODO

Export to various formats