# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 16:31:02 2025

@author: Aleksandr.Mikhailov
"""

from core.management.commands.generic_command import CSVImportCommand
from marine_cargo.utils.loaders.location_loader import LocationLoader


class Command(CSVImportCommand):
    loader_class = LocationLoader
