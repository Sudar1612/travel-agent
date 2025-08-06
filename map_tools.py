from agno.tools import Toolkit

class GoogleMapsTool(Toolkit):
    def __init__(self,api_key):
        super().__init__(name='google_maps_tool')
        self.api_key = api_key
        self.base_url = 'https://maps.googleapis.com/maps/api'
        self.register(self.get_place_maps_url)
    

    # search the places and return the places url
    def get_place_maps_url(self,place_name):
        return None