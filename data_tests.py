import unittest
import data


class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cats_data = data.Data()

    def test_get_cats(self):
        self.assertIsInstance(self.cats_data.get_cats(), str)

        parameters = {
            'attribute': 'name',
            'order': 'asc',
            'offset': '5',
            'limit': '6',
        }
        self.assertIsInstance(self.cats_data.get_cats(parameters), str)

        parameters = {
            'attribute': 'name',
            'order_invalid': 'asc',
            'offset': '5',
            'limit': '6',
        }
        self.assertIsInstance(self.cats_data.get_cats(parameters), str)

    def test_add_cat(self):
        self.assertIsInstance(self.cats_data.add_cat(dict()), str)

        parameters = {
            'attribute': 'name',
            'order': 'asc',
            'offset': '5',
            'limit': '6',
        }
        self.assertIsInstance(self.cats_data.add_cat(parameters), str)

        parameters = {
            'name': 'Tihon',
            'color': 'red & white',
            'tail_length': '15',
            'whiskers_length': '12',
        }
        self.assertIsInstance(self.cats_data.add_cat(parameters), str)
