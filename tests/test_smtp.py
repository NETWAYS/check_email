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
        self.assertIsNotNone(smtp.smtpcon)

        smtp.disconnect()
        self.assertIsNone(smtp.smtpcon)

    def test_send(self):

        smtp = SmtpConnection("localhost",
                              "1234",
                              "username",
                              "password",
                              "sender",
                              "receiver")

        smtp.smtpcon = mock.MagicMock()
        smtp.send()

        expected = ('sender', 'receiver', 'Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nFrom: sender\nTo: receiver\nSubject: ZYvO3a\nX-Custom-Tag: Email-Check-Icinga\n\nThis email is for monitoring.\nDo not reply.')
        actual = smtp.smtpcon.sendmail.call_args.args

        self.assertTrue('This email is for monitoring' in actual[2])
