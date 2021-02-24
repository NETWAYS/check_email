#!/usr/bin/env python3

import unittest
import unittest.mock as mock
import sys

sys.path.append('..')

from check_email import plugin_exit
from check_email import parse_arguments

class UtilTest(unittest.TestCase):

    @mock.patch('builtins.print')
    def test_plugin_exit(self, mock_print):
        with self.assertRaises(SystemExit) as actual:
            plugin_exit("OK", 0)
        self.assertEqual(actual.exception.code, 0)

        with self.assertRaises(SystemExit) as actual:
            plugin_exit("WARNING", 1)
        self.assertEqual(actual.exception.code, 1)

        with self.assertRaises(SystemExit) as actual:
            plugin_exit("CRITICAl", 2)
        self.assertEqual(actual.exception.code, 2)

    def test_parse_arguments_default(self):
        args = [
            '--reply-name',
            'foo',
            '--smtp-host',
            'foo',
            '--smtp-user',
            'foo',
            '--smtp-password',
            'foo',
            '--imap-host',
            'foo',
            '--imap-user',
            'foo',
            '--imap-password',
            'foo',
            '--sender',
            'foo',
            '--receiver',
            'foo'
        ]

        actual = parse_arguments(args)
        self.assertEqual(actual.sender, 'foo')
        self.assertNotEqual(actual.receiver, 'bar')
        # Check for Default subject
        self.assertTrue('check_email' in actual.subject)


    def test_parse_arguments_subject(self):
        args = [
            '--subject',
            'foobarforunittest',
            '--reply-name',
            'foo',
            '--smtp-host',
            'foo',
            '--smtp-user',
            'foo',
            '--smtp-password',
            'foo',
            '--imap-host',
            'foo',
            '--imap-user',
            'foo',
            '--imap-password',
            'foo',
            '--sender',
            'foo',
            '--receiver',
            'foo'
        ]

        actual = parse_arguments(args)
        self.assertEqual(actual.subject, 'foobarforunittest')
