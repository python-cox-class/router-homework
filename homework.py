import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

engine = sa.create_engine('sqlite:///test.db')
# For mysql, use something like 'mysql+mysqldb://root:foo@127.0.0.1:3306/test'
Session = sessionmaker(bind=engine)

import hw_model as M

M.Base.metadata.create_all(bind=engine, checkfirst=True)