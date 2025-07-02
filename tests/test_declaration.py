from unittest.mock import MagicMock

import pytest

from app.services import declaration


def test_validate_sheet_names_success():
    declaration.validate_sheet_names({'declaration_form', 'bl_breakdown'})


def test_validate_sheet_names_failure():
    with pytest.raises(ValueError):
        declaration.validate_sheet_names({'wrong_sheet'})


def test_create_ports_creates_expected():
    db = MagicMock()
    summary = {
        'loadport_locality': 'Houston',
        'loadport_country': 'USA',
        'disport_locality': 'Rotterdam',
        'disport_country': 'Netherlands'
    }

    db_port = MagicMock()
    db_port.id = 123
    declaration.crud.upsert_port = MagicMock(return_value=db_port)

    ports = declaration.create_ports(db, summary)

    assert ports['loadport_locality'] == 123
    assert ports['disport_locality'] == 123
    assert declaration.crud.upsert_port.call_count == 2
