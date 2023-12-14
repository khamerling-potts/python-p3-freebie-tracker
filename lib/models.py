from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, backref, Query, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy


convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship("Freebie", backref="company")
    devs = association_proxy("freebies", "dev", creator=lambda dv: Freebie(dev=dv))

    def __repr__(self):
        return f"<Company {self.id}>"

    # don't forget to add and commit this freebie to session
    def give_freebie(self, dev, item_name, value, session):
        session.add(
            Freebie(item_name=item_name, value=value, company_id=self.id, dev_id=dev.id)
        )
        session.commit()

    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()


class Dev(Base):
    __tablename__ = "devs"

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    freebies = relationship("Freebie", backref="dev")
    companies = association_proxy(
        "freebies", "company", creator=lambda cp: Freebie(company=cp)
    )

    def __repr__(self):
        return f"<Dev {self.id}>"

    def received_one(self, item_name):
        matching_freebies = [
            freebie for freebie in self.freebies if freebie.item_name == item_name
        ]
        return len(matching_freebies) > 0

    def give_away(self, dev, freebie, session):
        freebie_owner = session.query(Dev).filter(Dev.id == freebie.dev_id).first()
        if freebie_owner.id == self.id:
            freebie.dev_id = dev.id
            session.add(freebie)
            session.commit()


class Freebie(Base):
    __tablename__ = "freebies"
    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    dev_id = Column(Integer(), ForeignKey("devs.id"))
    company_id = Column(Integer(), ForeignKey("companies.id"))

    def __repr__(self):
        return f"id={self.id}, dev_id={self.dev_id}, company_id={self.company_id}"

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
