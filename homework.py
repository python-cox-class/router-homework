import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

import hw_model as M

engine = sa.create_engine('sqlite:///test.db')
# For mysql, use something like 'mysql+mysqldb://root:foo@127.0.0.1:3306/test'
Session = sessionmaker(bind=engine)


def create_database():
    M.Base.metadata.create_all(bind=engine, checkfirst=True)


def add_link_router():
    engine.echo = True
    session = Session()
    link1 = M.Link(netmask='192.168.0.0/16')
    link2 = M.Link(netmask='192.169.0.0/16')
    rtr = M.Router(address='http://somewhere')
    session.add(link1)
    session.add(link2)
    session.add(rtr)
    session.flush()
    session.commit()


def link_them():
    session = Session()
    rtr = session.query(M.Router).one()
    links = session.query(M.Link).all()
    for link in links:
        rtr.interfaces.append(M.Interface(link=link))
    session.flush()
    session.commit()

print 'Create DB'
create_database()

print 'Add links & router'
add_link_router()

print 'Link them '
link_them()
