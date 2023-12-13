#!/usr/bin/env python3

# Script goes here!
from random import choice

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Dev, Company, Freebie

engine = create_engine("sqlite:///freebies.db")
Session = sessionmaker(bind=engine)
session = Session()


def create_records():
    freebies = [Freebie() for i in range(100)]
    companies = [Company() for i in range(30)]
    devs = [Dev() for i in range(60)]
    session.add_all(freebies + companies + devs)
    session.commit()
    return freebies, companies, devs


def delete_records():
    session.query(Freebie).delete()
    session.query(Company).delete()
    session.query(Dev).delete()
    session.commit()


def relate_one_to_many(freebies, companies, devs):
    for freebie in freebies:
        freebie.company = choice(companies)
        freebie.dev = choice(devs)
    session.add_all(freebies)
    session.commit()
    return freebies, companies, devs


if __name__ == "__main__":
    delete_records()
    freebies, companies, devs = create_records()
    freebies, companies, devs = relate_one_to_many(freebies, companies, devs)
