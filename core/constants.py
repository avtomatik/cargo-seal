INDEX_MAP = {}

DEFAULT_INDEX = [
    'deal_number',
    'insured',
    'address',
    'counterparty',
    'beneficiary_address',
    'loadport_locality',
    'loadport_country',
    'disport_locality',
    'disport_country',
    'vessel',
    'imo',
    'date_built',
    'surveyor_loadport',
    'surveyor_disport',
    'subject_matter_insured',
    'provisional',
    'weight_metric',
    'ccy',
    'basis_of_valuation',
    'sum_insured'
]

CYRILLIC_IN_LATIN = (
    'a,b,v,g,d,e,zh,z,i,y,k,l,m,n,o,p,r,s,t,u,f,kh,ts,ch,sh,shch,,y,,e,yu,ya,'
    ',yo'
)

CYRILLIC_TO_LATIN = {
    chr(idx): latin
    for idx, latin in enumerate(CYRILLIC_IN_LATIN.split(','), start=1072)
}

MAX_LENGTH_CCY = 3

MAX_LENGTH_UNIT = 16

MAX_LENGTH_REF = 32

MAX_LENGTH_CHAR = 64

MAX_LENGTH_SLUG = 128

MAX_LENGTH_TEXT = 256

SHEET_NAMES_EXPECTED = {'declaration_form', 'bl_breakdown'}
