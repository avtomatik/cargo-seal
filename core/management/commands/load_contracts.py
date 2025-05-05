# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:16:43 2025

@author: Aleksandr.Mikhailov
"""

from core.management.commands.generic_command import CSVImportCommand
from marine_cargo.utils.loaders.contract_loader import ContractLoader


class Command(CSVImportCommand):
    loader_class = ContractLoader
