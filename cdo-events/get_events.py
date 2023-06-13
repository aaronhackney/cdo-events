import os
import logging
import argparse
import requests


class CDO:
    """
    CDO Base class that contains common CDO attributes and methods
    """

    def __init__(self, api_key: str, cdo_region: str) -> None:
        self.region = self.get_region_endpoint(cdo_region)
        self.http_session = requests.Session()
        self.set_headers(api_key)  # TODO: move to postinit

    def get_region_endpoint(self, cdo_region: str) -> None:
        """Set the api endpoint based on the region of the CDO deployment"""
        if cdo_region.lower() == "us":
            return "www.defenseorchestrator.com"
        elif cdo_region.lower() == "eu":
            return "www.defenseorchestrator.eu"
        elif cdo_region.lower() == "apj":
            return "apj.cdo.cisco.com"

    def set_headers(self, token):
        """Helper function to set the auth token and accept headers in the API request"""
        if "Authorization" in self.http_session.headers:
            del self.http_session.headers["Authorization"]
        self.http_session.headers["Authorization"] = f"Bearer {token.strip()}"
        self.http_session.headers["Accept"] = "application/json"
        self.http_session.headers["Content-Type"] = "application/json;charset=utf-8"


class CDOEvents(CDO):
    def __init__(self, api_key, cdo_region):
        CDO.__init__(self, api_key, cdo_region)

    def get_background_search_list(self) -> list:
        """Get a list of files that have been created by scheduled background searches"""
        api_response = self.http_session.get(
            url="https://" + self.region + "/swc/v1/download-status",
            params={"per_tenant": "true"},
            headers=self.http_session.headers,
        )
        if api_response.text:
            return api_response.json()

    def download_event_file(self, file_url: str):
        """ Retrieve the given file from the S3 bucket"""
        http_session = requests.Session()
        r = http_session.get(
            url=file_url,
        )
        return r.content


def main(api_key: str, file_prefix: str, download_dir: str):
    """ Download files with a matching prefix, only if we have not already downloaded them before"""
    events = CDOEvents(api_key=api_key, cdo_region="us")
    logging.warning(
        f"Getting events files from CDO with file prefix {file_prefix}...")
    event_list = events.get_background_search_list()
    for event_file in event_list['download_status']:
        # Only download files with the given prefix/name

        if event_file['file_name'].lower().startswith(file_prefix.lower()):
            # Only download the file if we have not already downloaded it
            if not os.path.isfile(f"{download_dir}/{event_file['file_name']}"):
                logging.warning(
                    f"Downloading events file {event_file['file_name']}...")
                file_contents = events.download_event_file(
                    event_file['download_url'])
                open(
                    f"{download_dir}/{event_file['file_name']}", 'wb').write(file_contents)
                logging.warning(
                    f"{download_dir}/{event_file['file_name']} written to disk")
            else:
                logging.warning(
                    f"{download_dir}/{event_file['file_name']} file exists - skipping")


if __name__ == "__main__":
    import sys
    test = sys.argv
    parser = argparse.ArgumentParser(
        prog='get_events.py', description='Tested with python 3.10.4')
    parser.add_argument('--prefix', type=str, required=True,
                        help="'--prefix abc123' The filename prefix to match for download")
    parser.add_argument('--data_dir', type=str, required=True,
                        help="'--data_dir /tmp/mydata' The download directory for the event files")
    args = parser.parse_args()

    api_key = os.environ.get('CDO_API_KEY')

    main(api_key, args.prefix, args.data_dir)
