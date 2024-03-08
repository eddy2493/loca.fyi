import requests
from datetime import date

class ImmoScout24API:
    """A class to interact with the ImmoScout24 API to fetch property listings."""
    
    def __init__(self):
        self.base_url = "https://rest-api.immoscout24.ch/v4/de"
        self.headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.6',
            'origin': 'https://www.immoscout24.ch',
            'referer': 'https://www.immoscout24.ch/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        }

    def _get_immoscout_location_id(self, zip_code=2502):
        """Retrieve the location ID for a given ZIP code."""
        params = {'term': zip_code}
        response = requests.get(f'{self.base_url}/locations', params=params, headers=self.headers)
        id_request = response.json()
        if id_request:
            return id_request[0]['id']
        return None

    def get_number_of_listings(self, zip_code=2501, offer_type='RENT'):
        """Get the number of listings for a given ZIP code and offer type."""
        immoscout_location_id = self._get_immoscout_location_id(zip_code)
        if immoscout_location_id:
            params = {
                's': 1,
                't': 1 if offer_type == 'RENT' else 2,
                'l': immoscout_location_id
            }
            response = requests.get(f'{self.base_url}/serpsearchfilters', params=params, headers=self.headers)
            return response.json()['searchMetaData']['totalMatches']
        return 0

    def get_listings(self, zip_code=2501, offer_type='RENT'):
        """Fetch listings for a given ZIP code and offer type."""
        immoscout_location_id = self._get_immoscout_location_id(zip_code)
        if immoscout_location_id:
            params = {
                's': 1,
                't': 1 if offer_type == 'RENT' else 2,
                'l': immoscout_location_id,
                'inp': 1
            }
            properties = []
            page = 1
            while True:
                self.headers['is24-meta-pagenumber'] = str(page)
                response = requests.get(f'{self.base_url}/properties', params=params, headers=self.headers).json()
                properties.extend(response['properties'])
                if page >= response['pagingInfo']['totalPages']:
                    break
                page += 1
            return properties

# Example usage
if __name__ == "__main__":
    api = ImmoScout24API()
    print(api.get_listings(zip_code=8049, offer_type='RENT'))
