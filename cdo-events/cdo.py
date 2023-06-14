
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

    def download_event_file(self, file_url: str) -> bytes:
        """ Retrieve the given file from the S3 bucket"""
        http_session = requests.Session()
        r = http_session.get(
            url=file_url,
        )
        return r.content
