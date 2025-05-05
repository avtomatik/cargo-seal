# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:39:27 2025

@author: Aleksandr.Mikhailov
"""

from core.management.commands.generic_command import CSVImportCommand
from marine_cargo.utils.loaders.policy_loader import PolicyLoader


class Command(CSVImportCommand):
    loader_class = PolicyLoader
