# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 22:15:36 2025

@author: Aleksandr.Mikhailov
"""

from core.management.commands.generic_command import CSVImportCommand
from marine_cargo.utils.loaders.document_loader import DocumentLoader


class Command(CSVImportCommand):
    loader_class = DocumentLoader
