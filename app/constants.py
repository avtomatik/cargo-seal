from pathlib import Path

CYRILLIC_IN_LATIN = (
    'a,b,v,g,d,e,zh,z,i,y,k,l,m,n,o,p,r,s,t,u,f,kh,ts,ch,sh,shch,,y,,e,yu,ya,'
    ',yo'
)

CYRILLIC_TO_LATIN = {
    chr(idx): latin
    for idx, latin in enumerate(CYRILLIC_IN_LATIN.split(','), start=1072)
}

SHEET_NAMES_EXPECTED = {'declaration_form', 'bl_breakdown'}

CLASSIFICATION_SOCIETIES_IACS = {
    'American Bureau of Shipping',
    'Bureau Veritas Marine & Offshore SAS',
    'China Classification Society',
    'Croatian Register of Shipping',
    'DNV AS',
    'Indian Register of Shipping',
    'Korean Register',
    "Hellenic Lloyd's S.A.",
    "Lloyd's Register (Romania) Srl",
    "Lloyd's Register Asia",
    "Lloyd's Register Central and South America Limited",
    "Lloyd's Register Classification Society (China) Co., Ltd.",
    "Lloyd's Register DOO Beograd",
    "Lloyd's Register EMEA",
    "Lloyd's Register Egypt LLC",
    "Lloyd's Register Gozetim Ltd. Sti.",
    "Lloyd's Register Group Limited",
    "Lloyd's Register Marine and Offshore India LLP",
    "Lloyd's Register Maritiem Belgie BV",
    "Lloyd's Register North America Inc.",
    "Lloyd's Register Singapore Pte. Ltd.",
    "Lloyd's Register do Brasil Ltda",
    'Nippon Kaiji Kyokai',
    'Polski Rejestr Statkow',
    'RINA SERVICES S.p.A.'
}

CLASSES_AGREED = CLASSIFICATION_SOCIETIES_IACS | set(
    ['Russian Maritime Register of Shipping']
)

BASE_DIR = Path(__file__).resolve().parents[1]

FIXTURE_DIR = BASE_DIR / 'app' / 'fixtures'

TEMPLATE_DIR = BASE_DIR / 'templates'

COL_FILE_NAME = 'columns.yaml'

GEN_FILE_NAME = 'config.yaml'

COL_FILE_PATH = BASE_DIR / 'config' / COL_FILE_NAME

GEN_FILE_PATH = BASE_DIR / 'config' / GEN_FILE_NAME
