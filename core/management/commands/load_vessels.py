# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 17:42:06 2025

@author: Aleksandr.Mikhailov
"""

from core.management.commands.generic_command import CSVImportCommand
from marine_cargo.utils.loaders.vessel_loader import VesselLoader


class Command(CSVImportCommand):
    loader_class = VesselLoader
