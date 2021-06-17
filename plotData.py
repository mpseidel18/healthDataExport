from geopy.geocoders import Nominatim
import healthdataInterpret
geolocator = Nominatim(user_agent="plotGooglHealthData")
location = geolocator.reverse("48.255024, 9.021384")
print(location.address)