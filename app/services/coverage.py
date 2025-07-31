from io import BytesIO
from pathlib import Path
from typing import Any

from mailmerge import MailMerge

from app import schemas


def generate_coverage_docx(coverage_obj: Any, template_path: Path) -> BytesIO:
    NBSP = '\u00A0'

    coverage_read = schemas.CoverageRead.model_validate(coverage_obj)

    merge_fields = {
        'deal_number': f'{coverage_read.shipment.deal_number}',
        'insured': f'{coverage_read.shipment.insured.name}',
        'address': f'{coverage_read.shipment.insured.address}',
        'beneficiary': 'To Order',
        'beneficiary_address': 'To Order',
        'vessel': f'{coverage_read.shipment.vessel.name}',
        'imo': f'{coverage_read.shipment.vessel.imo}',
        'year_built': f'{coverage_read.shipment.vessel.year_built}',
        'loadport': coverage_read.shipment.loadport.full_name,
        'disport': coverage_read.shipment.disport.full_name,
        'subject_matter_insured': f'{coverage_read.shipment.product_names}',
        'bl_number': coverage_read.shipment.bills_of_lading_display,
        'date': f'{coverage_read.date:%d{NBSP}%B{NBSP}%Y}',
        'bl_date': f'{coverage_read.date:%d{NBSP}%B{NBSP}%Y}',
        'policy_date': f'{coverage_read.policy.inception:%d{NBSP}%B{NBSP}%Y}',
        'weight_metric': f'{coverage_read.shipment.total_weight_mt:,.3f}',
        'sum_insured': f'USD{NBSP}{coverage_read.shipment.total_value_usd:,.2f}',
        'policy_number': f'{coverage_read.policy.number}',
        'basis_of_valuation': f'{1 + coverage_read.value_margin:.0%}',
        'surveyor_loadport': 'SGS Vostok Limited',
        'surveyor_disport': 'Unknown',
    }

    buffer = BytesIO()

    with MailMerge(template_path) as document:
        document.merge(**merge_fields)
        document.merge_rows('bl_number', merge_fields.get('bl_number'))
        document.write(buffer)

    buffer.seek(0)
    return buffer
