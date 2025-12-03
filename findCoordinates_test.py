from unittest import TestCase
from findCoordinates import findCoordinates


class Test(TestCase):
    def setUp(self):
        #Initialize with values that should return None
        self.test_api = findCoordinates("123 Main St")

    def test_find_coordinates(self):
        self.assertIsNone(self.test_api)

        #Test with invalid input (integer)
        self.test_api = findCoordinates(12345)
        self.assertIsNone(self.test_api)

        #Test by giving non-str key
        addresses = ["Portland, OR"]
        self.test_api = findCoordinates(addresses, 123)
        self.assertIsNone(self.test_api)

        #Test valid inputs using places I've visited
        addresses = ["738 Umi St, Honolulu, HI 96819",
                     "55 W 35th St, New York, NY 10001",
                     "Merianstraße 4, 5020 Salzburg, Austria",]

        self.expected_lat = [21.33388, 40.75005, 47.81142]
        self.expected_lng = [-157.88251, -73.98634, 13.05366]

        self.test_api = findCoordinates(addresses)
