#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 12:51:38 2025

@author: alexandermikhailov
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Class Responsible for Populating Database."""

    def handle(self, *args, **options):
        """Main Class Method."""

        call_command('load_locations', *args, **options)
        call_command('load_operators', *args, **options)
        call_command('load_parties', *args, **options)
        call_command('load_vessels', *args, **options)
        call_command('load_contracts', *args, **options)
        call_command('load_documents', *args, **options)
        call_command('load_policies', *args, **options)
        call_command('load_shipments', *args, **options)
        # TODO: For Possible Refactoring
        call_command('dump_shipments_uuids', *args, **options)
        call_command('load_coverage', *args, **options)
