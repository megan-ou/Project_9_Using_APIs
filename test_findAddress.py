from unittest import TestCase
from unittest import main

import shelve
from findAddress import findAddress
import math


class TestFindAddress(TestCase):
    def setUp(self) -> None:
        self.expected = shelve.open("expected_results")

    def tearDown(self) -> None:
        self.expected.close()

    def test_coordinates_unequal(self):
        self.assertTrue(findAddress((1, 2), (1, 2, 3)) is None)

    def test_non_tuple(self):
        self.assertTrue(findAddress(1, (2,)) is None)
        self.assertTrue(findAddress((1, ), 2) is None)
        self.assertTrue(findAddress(1, 2) is None)
        self.assertTrue(findAddress((33.8,), (-117.9,)) is not None)

    def test_coordinates_UP(self):
        expected = self.expected['test.address.UP']
        lat = tuple(expected['lat'].to_list())
        lng = tuple(expected['lng'].to_list())

        actual = findAddress(lat, lng)

        self.assertTrue(expected['address'].equals(actual['address']))

    def test_state_capitols(self):
        lat = tuple(self.expected['state_capitols']['reverse_geocode']['lat'])
        lng = tuple(self.expected['state_capitols']['reverse_geocode']['lng'])

        expected = self.expected['state_capitols']['reverse_geocode']['address_df']
        actual = findAddress(lat, lng)

        for i in range(len(lat)):
            with self.subTest(lat=lat[i], lng=lng[i]):
                print(f'lat: {lat[i]}, lng: {lng[i]}, sc: {actual["status_code"][i]}, addr: {actual["address"][i]}')
                self.assertEqual(expected['address'][i], actual['address'][i])
                self.assertEqual(expected['status_code'][i], actual['status_code'][i])


    def test_mlb_parks(self):
        lat = tuple(self.expected['mlb_parks']['reverse_geocode']['lat'])
        lng = tuple(self.expected['mlb_parks']['reverse_geocode']['lng'])

        expected = self.expected['mlb_parks']['reverse_geocode']['address_df']
        actual = findAddress(lat, lng)

        for i in range(len(lat)):
            with self.subTest(lat=lat[i], lng=lng[i]):
                self.assertEqual(expected['address'][i], actual['address'][i])
                self.assertEqual(expected['status_code'][i], actual['status_code'][i])

if __name__ == '__main__':
    rslt = main(verbosity=2, exit=False)