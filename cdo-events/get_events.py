import os
import gzip
import shutil
import logging
import argparse

from cdo import CDOEvents


def unzip_file(file_name, download_dir):
    """ Given a path and file, unzip the file and delete the original archive """
    with gzip.open(f"{download_dir}/{file_name}", 'rb') as f_in:
        with open(f"{download_dir}/{file_name.split('.')[0]}.csv", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            logging.warning(f"Data file {download_dir}/{file_name} unzipped")
    # Delete the archive once uncompressed
    os.remove(f"{download_dir}/{file_name}")
    logging.warning(f"Archive {download_dir}/{file_name} deleted")


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
                open(f"{download_dir}/{event_file['file_name']}", 'wb').write(file_contents)
                # Unzip the data file and delete the original archive
                unzip_file(event_file['file_name'], download_dir)
            else:
                logging.warning(f"{download_dir}/{event_file['file_name']} file exists - skipping")


def main(api_key: str, file_prefix: str, download_dir: str, cdo_region: str):
    download_files(api_key, file_prefix, download_dir, cdo_region)


if __name__ == "__main__":
    import sys
    parser = argparse.ArgumentParser(prog='get_events.py', description='Tested with python 3.10.4')
    parser.add_argument('--prefix', type=str, required=True,
                        help="'--prefix abc123' The filename prefix to match for download")
    parser.add_argument('--data_dir', type=str, required=True,
                        help="'--data_dir /tmp/mydata' The download directory for the event files")
    parser.add_argument('--region', type=str, default='us',
                        help="'--region [region]' us, eu, or apj region where your CDO tenant resides")
    args = parser.parse_args()
    api_key = os.environ.get('CDO_API_KEY')
    main(api_key, args.prefix, args.data_dir, args.region)
