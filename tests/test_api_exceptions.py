import unittest

from api_exceptions import ResourceNotFound, EndpointNotImplemented, BadRequest


class TestExceptions(unittest.TestCase):
    def test_exceptions(self):
        message = "Some message"
        for e in ResourceNotFound, EndpointNotImplemented, BadRequest:
            exception = e(message)
            self.assertEqual(exception.description, message)
