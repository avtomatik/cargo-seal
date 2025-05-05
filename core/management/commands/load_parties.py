# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 17:47:51 2025

@author: Aleksandr.Mikhailov
"""

from core.management.commands.generic_command import CSVImportCommand
from marine_cargo.utils.loaders.party_loader import PartyLoader


class Command(CSVImportCommand):
    loader_class = PartyLoader
