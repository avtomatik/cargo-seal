from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ⚙️ DATABASE URL FORMAT:
# For PostgreSQL: 'postgresql://user:password@localhost/dbname'
# For SQLite: 'sqlite:///./test.db'
DATABASE_URL = 'sqlite:///./marine_cargo.db'

# If using SQLite, this helps avoid threading issues
connect_args = {'check_same_thread': False} if 'sqlite' in DATABASE_URL else {}

# 🚀 SQLAlchemy Engine & Session
engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🧱 Base class for models
Base = declarative_base()
