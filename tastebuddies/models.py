from sqlalchemy import (
    Table,
    Column,
    Integer,
    Text,
    ForeignKey,
    Boolean
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    validates,
    )


from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


usertaste_table = Table('user_profile', Base.metadata,
                        Column('users', Integer, ForeignKey('users.id')),
                        Column('profile', Integer, ForeignKey('profile.id'))
                        )


userdiet_table = Table('user_diet', Base.metadata,
                       Column('users', Integer, ForeignKey('users.id')),
                       Column('profile', Integer, ForeignKey('diet.id'))
                       )


usercost_table = Table('user_cost', Base.metadata,
                       Column('users', Integer, ForeignKey('users.id')),
                       Column('profile', Integer, ForeignKey('cost.id'))
                       )


groupdiscussion_table = Table('group_discussion', Base.metadata,
                              Column('group', Integer, ForeignKey('group.id')),
                              Column('discussion', Integer, ForeignKey(
                                     'discussion.id'))
                              )

groupage_table = Table('group_age', Base.metadata, Column('group', Integer,
                       ForeignKey('group.id')), Column('agegroup', Integer,
                       ForeignKey('agegroup.id'))
                       )

groupuser_table = Table('group_user', Base.metadata, Column('group', Integer,
                        ForeignKey('group.id')), Column('users', Integer,
                        ForeignKey('users.id'))
                        )


class Table(object):
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def write(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls(**kwargs)
        session.add(instance)
        return instance


class User(Base, Table):
    __tablename__ = 'users'
    username = Column(Text, nullable=False, unique=True)
    firstname = Column(Text, nullable=False)
    lastname = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    confirmed = Column(Boolean)
    age = Column(Integer, ForeignKey('agegroup.id'))
    user_location = Column(Integer, ForeignKey('location.id'))
    food_profile = relationship('Profile', secondary=usertaste_table)
    diet_restrict = relationship('Diet', secondary=userdiet_table)
    cost_restrict = relationship('Cost', secondary=usercost_table)
    user_groups = relationship('Group', secondary=groupuser_table)
    restaurants = Column(Text)

    @validates('email')
    def validate_email(self, key, email):
        try:
            assert '@' in email
            assert '.' in email
            return email
        except:
            raise TypeError('Please enter a vaild email address')

    @classmethod
    def lookup_user(cls, username, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(username=username).all()

    def __repr__(self):
        return "<User({} {}, username={})>".format(self.firstname,
                                                   self.lastname,
                                                   self.username)


class Profile(Base, Table):
    __tablename__ = 'profile'
    taste = Column(Text)

    def __repr__(self):
        return "<Taste(%s)>" % (self.taste)


class AgeGroup(Base, Table):
    __tablename__ = 'agegroup'
    age_group = Column(Text)

    def __repr__(self):
        return "<Age(%s)>" % (self.age_group)


class Location(Base, Table):
    __tablename__ = 'location'
    city = Column(Text)

    def __repr__(self):
        return "<Location(%s)>" % (self.city)


class Cost(Base, Table):
    __tablename__ = 'cost'
    cost = Column(Text)

    def __repr__(self):
        return "<Cost(%s)>" % (self.cost)


class Diet(Base, Table):
    __tablename__ = 'diet'
    diet = Column(Text)

    def __repr__(self):
        return "<Dietary Preference(%s)>" % (self.diet)


class Group(Base, Table):
    __tablename__ = 'group'
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(Integer, ForeignKey('location.id'))
    discussion = relationship('Discussion', secondary=groupdiscussion_table)
    group_admin = relationship("Admin", uselist=False)

    def __repr__(self):
        return "<Group(%s, location=%s)>" % (self.name, self.location)


class Discussion(Base, Table):
    __tablename__ = 'discussion'
    discussion_title = Column(Text)

    def __repr__(self):
        return "<Discussion(%s)>" % (self.discussion_title)


class Post(Base, Table):
    __tablename__ = 'post'
    discussionpost = Column(Integer, ForeignKey('discussion.id'))

    def __repr__(self):
        return "<Post(%s)>" % (self.discussionpost)


class Admin(Base, Table):
    __tablename__ = 'admin'
    users = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('group.id'))

    def __repr__(self):
        return "<Admin(%s)>" % (self.users)
