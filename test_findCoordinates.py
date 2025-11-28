from unittest import TestCase
from unittest import main

import shelve
from findCoordinates import findCoordinates
import math


class TestFindCoordinates(TestCase):

    def setUp(self) -> None:
        self.expected = shelve.open("expected_results")

    def tearDown(self) -> None:
        self.expected.close()

    def test_address_UP(self):
        actual = findCoordinates(['5000 N. Willamette Blvd, Portland, OR, 97203'])
        expected = self.expected['test.address.UP']

        for i in range(len(expected)):
            with self.subTest(row=i):
                self.assertAlmostEqual(expected['lat'][i], actual['lat'][i])
                self.assertAlmostEqual(expected['lng'][i], actual['lng'][i])
                self.assertEqual(expected['address'][i], actual['address'][i])
                self.assertEqual(expected['status_code'][i], actual['status_code'][i])

    def test_address_invalid(self):
        actual = findCoordinates(['???'])
        expected = self.expected['test.address.invalid']

        for i in range(len(expected)):
            with self.subTest(row=i):
                self.assertTrue(math.isnan(actual['lng'][i]))
                self.assertTrue(math.isnan(actual['lng'][i]))
                self.assertEqual(expected['address'][i], actual['address'][i])
                self.assertEqual(expected['status_code'][i], actual['status_code'][i])

    def test_state_capitols(self):
        addresses = self.expected['state_capitols']['geocode']['addresses']
        expected = self.expected['state_capitols']['geocode']['coord_df']
        actual = findCoordinates(list(addresses))

        for i in range(len(addresses)):
            with self.subTest(addr=addresses[i]):
                self.assertAlmostEqual(expected['lat'][i], actual['lat'][i])
                self.assertAlmostEqual(expected['lng'][i], actual['lng'][i])
                self.assertEqual(expected['address'][i], actual['address'][i])
                self.assertEqual(expected['status_code'][i], actual['status_code'][i])

    def test_mlb_parks(self):
        addresses = self.expected['mlb_parks']['geocode']['addresses']
        expected = self.expected['mlb_parks']['geocode']['coord_df']
        actual = findCoordinates(list(addresses))

        for i in range(len(addresses)):
            with self.subTest(addr=addresses[i]):
                self.assertAlmostEqual(expected['lat'][i], actual['lat'][i])
                self.assertAlmostEqual(expected['lng'][i], actual['lng'][i])
                self.assertEqual(expected['address'][i], actual['address'][i])
                self.assertEqual(expected['status_code'][i], actual['status_code'][i])


if __name__ == '__main__':
    rslt = main(verbosity=2, exit=False)