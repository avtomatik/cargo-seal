# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 11:54:40 2025

@author: Aleksandr.Mikhailov
"""

from core.management.commands.generic_command import CSVImportCommand
from marine_cargo.utils.loaders.operator_loader import OperatorLoader


class Command(CSVImportCommand):
    loader_class = OperatorLoader
