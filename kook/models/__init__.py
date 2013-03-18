# -*- coding: utf-8 -*-

from uuid import uuid4
import cryptacular.bcrypt
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import Everyone, Allow, ALL_PERMISSIONS, Deny
from kook.security import VOTE_ACTIONS

DBSession = scoped_session(sessionmaker(
    extension=ZopeTransactionExtension()))

UPVOTE = 1
DOWNVOTE = -1
UNDO_VOTE = 0

# tuple explained: ({author rep change}, {voter rep change},
#                   {required rep})
VOTE_REP_MAP = {
    UPVOTE: (10, 0, 15),
    DOWNVOTE: (-2, -1, 125)
}
UPVOTE_REWARD = VOTE_REP_MAP[UPVOTE][0]
DOWNVOTE_PENALTY = VOTE_REP_MAP[UPVOTE][0]
DOWNVOTE_COST = VOTE_REP_MAP[UPVOTE][2]

FRACTIONS = {
    0.5: u'½',
    0.33: u'⅓',
    0.25: u'¼',
    0.2: u'⅕'
}
crypt = cryptacular.bcrypt.BCRYPTPasswordManager()


def generate_id():
    return str(uuid4())


def generate_hash(password):
    return crypt.encode(password)


def form_msg(acl):
    try:
        if acl.ace == (Deny, Everyone, VOTE_ACTIONS):
            return u'Для голосования нужно зарегистрироваться и войти на сайт'
        if acl.ace == (Deny, acl.context.author.id, VOTE_ACTIONS):
            return u'Нельзя голосовать за свои рецепты'
        if acl.ace == (Deny, 'registered', 'upvote'):
            return u'У вас недостаточно репутации, необходимо %s'\
                   % VOTE_REP_MAP[UPVOTE][1]
        if acl.ace == (Deny, 'registered', 'downvote'):
            return u'У вас недостаточно репутации, необходимо %s'\
                   % VOTE_REP_MAP[DOWNVOTE][1]
        else:
            return u'действие: %s; кому %s; привилегия: %s' % acl.ace
    except AttributeError:
        pass


class Entity(object):
    """
    Basic (abstract) class for all entities
    """
    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def save(self):
        DBSession.merge(self)

    def add(self):
        DBSession.add(self)

    def delete(self):
        DBSession.delete(self)

    def revert(self):
        DBSession.rollback()

    @classmethod
    def fetch(cls, primary):
        return DBSession.query(cls).get(primary)

    @classmethod
    def fetch_all(cls, **kwargs):
        query = DBSession.query(cls)
        if 'order' in kwargs:
            query = query.order_by(getattr(cls, kwargs['order']))
        return query.all()


class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, ('read')),
        (Allow, 'registered', ('create', 'update', 'delete',
                               'vote', 'comment', 'dashboard')),
        (Allow, 'admins', ALL_PERMISSIONS),
        (Deny, Everyone, ALL_PERMISSIONS)
    ]

    def __init__(self, request):
        pass  # pragma: no cover