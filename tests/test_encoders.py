import unittest
import datetime
from encoders import DateEncoder


class TestExceptions(unittest.TestCase):
    def test_encoder(self):
        de = DateEncoder()
        self.assertEqual(type(de.default(datetime.datetime.now())), str)
        self.assertEqual(type(de.default(datetime.date.today())), str)
