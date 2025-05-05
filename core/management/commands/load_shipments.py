# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:59:19 2025

@author: Aleksandr.Mikhailov
"""

from core.management.commands.generic_command import CSVImportCommand
from marine_cargo.utils.loaders.shipment_loader import ShipmentLoader


class Command(CSVImportCommand):
    loader_class = ShipmentLoader
