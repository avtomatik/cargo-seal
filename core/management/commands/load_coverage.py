# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:13:17 2025

@author: Aleksandr.Mikhailov
"""

from core.management.commands.generic_command import CSVImportCommand
from marine_cargo.utils.loaders.coverage_loader import CoverageLoader


class Command(CSVImportCommand):
    loader_class = CoverageLoader
