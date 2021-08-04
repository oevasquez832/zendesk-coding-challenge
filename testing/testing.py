#Testing script for ticket_viewer.py

import unittest
from ticket_viewey import formatted_name

class TicketsTestCase(unittest.TestCase):

    def test_input(self):
        result = check_input("select")s
        self.assertEqual(result, "select")

    #def test_response(self):
    #    result = check_status('select')
    #    self.assertEqual(result, response.json())