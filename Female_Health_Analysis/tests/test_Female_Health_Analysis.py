#!/usr/bin/env python

"""Tests for `Female_Health_Analysis` package."""


import unittest
from click.testing import CliRunner

from Female_Health_Analysis import Female_Health_Analysis
from Female_Health_Analysis import cli


class TestFemale_health_analysis(unittest.TestCase):
    """Tests for `Female_Health_Analysis` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'Female_Health_Analysis.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
