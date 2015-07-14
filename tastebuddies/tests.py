# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import models
import os
import pytest
from sqlalchemy import create_engine

TEST_DATABASES_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://meslater:@localhost:5432/test-taste-buddies'
)
os.environ['DATABASE_URL'] = TEST_DATABASES_URL


# you will want to make a fixture that creates an app

@pytest.fixture(scope='session')
def connection(request):
    engine = create_engine(TEST_DATABASES_URL)
    models.Base.metadata.create_all(engine)
    connection = engine.connect()
    models.DBSession.registry.clear()
    models.DBSession.configure(bind=connection)
    models.Base.metadata.bind = engine
    request.addfinalizer(models.Base.metadata.drop_all)
    return connection


@pytest.fixture()
def db_session(request, connection):
    from transaction import abort
    trans = connection.begin()
    request.addfinalizer(trans.rollback)
    request.addfinalizer(abort)

    from models import DBSession
    return DBSession


@pytest.fixture()
def create_user(db_session):
    profile = models.Profile.write(
        taste='spicy'
    )
    age = models.AgeGroup.write(
        age_group='18-24'
    )
    location = models.Location.write(
        city='Seattle'
    )
    cost = models.Cost.write(
        cost='expensive'
    )
    diet = models.Diet.write(
        diet='vegan'
    )
    user = models.User.write(
        username='BobRocks',
        firstname='Bob',
        lastname='Jones',
        password='secret',
        email='bob.jones@gmail.com',
        restaurants='Chipotle',
    )
    db_session.flush()
    return user, profile, age, location, cost, diet


def test_create_user(create_user, db_session):
    create_user
    assert len(db_session.query('User').all()) == 1
