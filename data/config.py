from pathlib import Path


DB_NAME = 'students.db'
ROOT_FOLDER = Path(__file__).parent.resolve()
DB_PATH = ROOT_FOLDER / 'db' / DB_NAME

DB_TYPE = 'sqlite'

DB_CONNECTION_URL = f'{DB_TYPE}:///{DB_PATH}'
