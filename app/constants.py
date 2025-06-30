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

CLASSES_AGREED = {'DNV', 'ABS', 'Lloyds', 'Bureau Veritas'}

BASE_DIR = Path(__file__).resolve().parents[1]

FIXTURE_DIR = BASE_DIR / 'app' / 'fixtures'

COL_FILE_NAME = 'columns.yaml'

GEN_FILE_NAME = 'config.yaml'

COL_FILE_PATH = BASE_DIR / 'config' / COL_FILE_NAME

GEN_FILE_PATH = BASE_DIR / 'config' / GEN_FILE_NAME
