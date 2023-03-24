#!/usr/bin/env python3

import unittest
import unittest.mock as mock
import sys
import time

sys.path.append('..')

from check_email import SmtpConnection

class SmtpTest(unittest.TestCase):

    def test_disconnect(self):

        smtp = SmtpConnection("localhost",
                              "1234",
                              "username",
                              "password",
                              "sender",
                              "receiver")

        smtp.smtpcon = mock.MagicMock()

        smtp.disconnect()
