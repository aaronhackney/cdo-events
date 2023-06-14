# get_events.py

## Prerequisites
1. The API key should be set as an environment variable in the OS shell.  
   e.g. export CDO_API_KEY="xxxxxxxxxxxxxx"
2. This script has been tested on python 3.10 but should work on any python 3.6+ versions
3. The following python libraries must be installed: requests

## CLI Arguments
 --prefix (required) is the file name prefix we wish to match. For example, if the scheduled background search filenames that we wish to download all start with IPS-EVENTS then we would pass `--prefix IPS-EVENTS` to the script  
 --data_dir (required) is the directory where we wish to download and store the event files.  
 Example: `--data_dir /tmp/myfiles` or `--data_dir c:\data\myfiles\`  
 --region (optional, default=us) The region where the CDO tenant resides. Choices are us, eu, or apj  
 Example: `--region apj`

## Help  
`python3 get_events.py -h`

## Example Usage:
1. setup virtual python environment
```
python3 -m venv  ~/envs/cdo-events
source ~/envs/cdo-events/bin/activate
pip3 install requests
```
2. Clone the git repo
```
git clone https://github.com/aaronhackney/cdo-events.git
```
3. Add your API key into the shell variable `CDO_API_KEY`
```
export CDO_API_KEY="YourCDOAPIKeyGoesHere"
```
4. Run the script (assumes your data directory exists)
```
cd cdo-events/cdo-events
python3 get_events.py --prefix AHACK-SNORT-EVENTS --data_dir /tmp/events
 