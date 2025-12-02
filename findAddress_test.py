from unittest import TestCase
from findAddress import findAddress

class Test(TestCase):
    def setUp(self):
        #Initialize with values that should return none
        self.test_api = findAddress(0,0)
    def test_find_address(self):
        self.assertIsNone(self.test_api)

        #Test tuples of different lengths
        lat = (123, 456)
        lng = (789,)
        self.test_api = findAddress(lat, lng)
        self.assertIsNone(self.test_api)

        #Test by giving non-str key
        lng = (789, 123)
        self.test_api = findAddress(lat, lng, 123)

        self.assertIsNone(self.test_api)

        #Test valid inputs using restaurants around the world (that I've been to!)
        lat = (45.582570910977424, 45.558978373215616, 40.642000053688996, 46.052259527301096, 35.70532284491928)
        lng = (-122.6866764383464,-122.65095367218755, -74.07729268834848, 14.512453943961237, 139.774277654516)
        self.expected_address = ["8202 North Denver Avenue, Portland, OR 97217",
                                 "1438 Northeast Alberta Street, Portland, OR 97211",
                                 "19 Hyatt Street, Staten Island, NY 10301",
                                 "Znamenjska ulica 4, 1000 Ljubljana",
                                 "東京, Kanto"]

        self.test_api = findAddress(lat, lng)

        for i in range(len(self.expected_address)):
            self.assertEqual(self.test_api["status_code"][i],200)
            self.assertEqual(self.test_api["address"][i],self.expected_address[i])
