#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 12:51:38 2025

@author: alexandermikhailov
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Command to orchestrate loading sample data into the database."""

    help = 'Load all sample data into the database in the correct order.'

    LOAD_COMMANDS = [
        'load_locations',
        'load_operators',
        'load_parties',
        'load_vessels',
        'load_contracts',
        'load_documents',
        'load_policies',
        'load_shipments',
        # TODO: For Possible Refactoring
        'dump_shipments_uuids',
        'load_coverage',
    ]

    def handle(self, *args, **options):
        """Call Each Command in the Predefined Order."""
        for command_name in self.LOAD_COMMANDS:
            self.stdout.write(
                self.style.NOTICE(f'Executing `{command_name}`...')
            )
            call_command(command_name, *args, **options)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully ran `{command_name}`')
            )
