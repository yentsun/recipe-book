from uuid import uuid4
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import Everyone, Allow, ALL_PERMISSIONS

DBSession = scoped_session(sessionmaker(
    extension=ZopeTransactionExtension()))

class Entity(object):
    """
    Basic (abstract) class for all entities
    """
    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def save(self):
        DBSession.merge(self)

    def delete(self):
        DBSession.delete(self)

    @classmethod
    def fetch(cls, primary):
        return DBSession.query(cls).get(primary)

    @classmethod
    def fetch_all(cls, **kwargs):
        return DBSession.query(cls).all()

    @classmethod
    def multidict_to_dict(cls, multidict):
        pass

    @classmethod
    def construct_from_dict(cls, cstruct, **kwargs):
        pass

    @classmethod
    def construct_from_multidict(cls, multidict, **kwargs):
        dict = cls.multidict_to_dict(multidict)
        return cls.construct_from_dict(dict, kwargs.get('localizer'))

    @classmethod
    def generate_id(cls):
        return str(uuid4())

class RootFactory(object):
    __acl__ = [(Allow, Everyone, ('read')),
               (Allow, 'registered', ('create', 'update', 'delete')),
               (Allow, 'admins', ALL_PERMISSIONS)]

    def __init__(self, request):
        pass  # pragma: no cover