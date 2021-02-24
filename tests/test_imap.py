#!/usr/bin/env python3

import unittest
import unittest.mock as mock
import sys
import time

sys.path.append('..')

from check_email import ImapConnection

class ImapTest(unittest.TestCase):

    def test_parse_received(self):

        imap = ImapConnection("localhost",
                              "1234",
                              "username",
                              "password",
                              "mailbox",
                              "subject",
                              "cleanup")

        actual = imap.parse_received("test")
        expected = int(time.time())
        self.assertEqual(actual, expected)

        actual = imap.parse_received("; Wed, 1 Jan 1986 01:01:01 -0100")
        expected = int(504928861)
        self.assertEqual(actual, expected)
