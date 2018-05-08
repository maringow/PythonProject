from sqlalchemy import create_engine, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base



meta = MetaData()
Base = declarative_base(metadata=meta)