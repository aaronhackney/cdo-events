import os
import gzip
import shutil
import logging
import argparse
from cdo import CDOEvents


def write_file(compressed_file, file_name, download_dir):
    """ Given a path and file, unzip the file in memory and save to disk """
    file_contents = gzip.decompress(compressed_file)
    with open(f"{download_dir}/{file_name}", 'wb') as f:
        f.write(file_contents)


def download_files(api_key: str, file_prefix: str, download_dir: str, cdo_region: str):
    """ Download files with a matching prefix, only if we have not already downloaded them before"""
    events = CDOEvents(api_key=api_key, cdo_region=cdo_region)
    event_list = events.get_background_search_list()
    for event_file in event_list['download_status']:
        # Only consider files with the given prefix/name
        if event_file['file_name'].lower().startswith(file_prefix.lower()):
            # Only download the file if we have not already downloaded and unzipped it
            if not os.path.isfile(f"{download_dir}/{event_file['file_name'].split('.')[0]}.csv"):
                logging.warning(f"Downloading events file {event_file['file_name']}...")
                file_contents = events.download_event_file(
                    event_file['download_url'])
                write_file(file_contents, f"{event_file['file_name'].split('.')[0]}.csv", download_dir)
            else:
                logging.warning(f"{download_dir}/{event_file['file_name']} file exists - skipping")


def main(api_key: str, file_prefix: str, download_dir: str, cdo_region: str):
    download_files(api_key, file_prefix, download_dir, cdo_region)


if __name__ == "__main__":
    import sys
    parser = argparse.ArgumentParser(prog='get_events.py', description='python3 get_events.py --help for arguments')
    parser.add_argument('--prefix', type=str, required=True,
                        help="--prefix abc123 - The filename prefix to match for download")
    parser.add_argument('--data_dir', type=str, required=True,
                        help="--data_dir /tmp/mydata - The download directory for the event files")
    parser.add_argument('--region', type=str, default='us',
                        help="--region eu - [us, eu, apj] CDO tenant region (default: us)")
    args = parser.parse_args()
    api_key = os.environ.get('CDO_API_KEY')
    main(api_key, args.prefix, args.data_dir, args.region)
