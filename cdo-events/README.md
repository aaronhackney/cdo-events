# get_events.py

## Prerequisites
1. The API key should be set as an environment variable in the OS shell.  
   e.g. export CDO_API_KEY="xxxxxxxxxxxxxx"
2. This script has been tested on python 3.10 but should work on any python 3.6+ versions
3. The following python libraries must be installed: requests, argparse

## CLI Arguments
 --prefix (required) is the file name prefix we wish to match. For example, if the scheduled background search filenames that we wish to download all start with IPS-EVENTS then we would pass `--prefix IPS-EVENTS` to the script  
 --data_dir (required) is the directory where we wish to download and store the event files. Example: `--data_dir /tmp/myfiles` or `--data_dir c:\data\myfiles\`

## Example Usage:  
`python3 get_events.py --prefix AHACK-SNORT-EVENTS --data_dir /tmp/events`
 