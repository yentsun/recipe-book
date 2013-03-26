import json
from hashlib import md5
from urllib import urlencode
from datetime import date, datetime
from colander import Invalid
from sqlalchemy import desc
from sqlalchemy.orm import mapper, relationship

from kook.models import (Entity, DBSession, VOTE_REP_MAP, generate_id,
                         generate_hash, UPVOTE, DOWNVOTE)
from kook.models.sqla_metadata import (profiles, rep_records, groups,
                                       user_favourites, user_groups, users)
from schemas import UserSchema, ProfileSchema, dont_check_current_nickname

PRIVGROUPS = {
    'upvoters': VOTE_REP_MAP[UPVOTE][1],
    'downvoters': VOTE_REP_MAP[DOWNVOTE][1]
}


class Group(Entity):

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return self.title


class Profile(Entity):
    """Profile for a user"""

    def __init__(self, nickname=None, real_name=None, birthday=None,
                 location=None, registration_day=None, rep=None):
        self.nickname = nickname
        self.real_name = real_name
        self.birthday = birthday
        self.location = location
        self.registration_day = registration_day or date.today()
        self.rep = rep or 1

    @classmethod
    def fetch(cls, user_id):
        """Fetch profile by user id"""
        return DBSession.query(cls).get(user_id)

    @classmethod
    def construct_from_multidict(cls, multidict, **kwargs):
        current_profile = kwargs.get('current_profile')
        skip_nickname = False
        if current_profile and current_profile.nickname ==\
                multidict.getone('nickname'):
            skip_nickname = True
        schema = ProfileSchema(after_bind=dont_check_current_nickname) \
            .bind(skip_nickname=skip_nickname)
        try:
            appstruct = schema.deserialize(multidict)
        except Invalid, e:
            return {'errors': e.asdict(),
                    'original_data': multidict.mixed()}
        if 'nickname' in appstruct:
            nickname = appstruct['nickname']
        else:
            nickname = current_profile.nickname
        profile = cls(nickname, appstruct['real_name'],
                      appstruct['birthday'], appstruct['location'])
        return profile


class User(Entity):
    """The user class"""

    def __init__(self, id_, email, password_hash, groups=None,
                 profile=None, favourite_titles=None):
        self.id = id_
        self.email = email
        self.password_hash = password_hash
        self.groups = groups or []
        self.profile = profile
        self.favourite_titles = favourite_titles or []

    def to_json(self):
        dict_ = {'id': self.id,
                 'display_name': self.display_name}
        return json.dumps(dict_)

    def check_password(self, password):
        from kook.models import crypt
        return crypt.check(self.password_hash, password)

    def generate_password(self):
        """Generate new password and send it to user email"""
        #TODO complete function
        return '000000'

    def add_rep(self, rep_value, subject, ref_object=None):
        """Add rep record with a subject and optional referenced object"""
        record = RepRecord(self.id, rep_value, subject, ref_object)
        record.save()

    def fetch_rep(self):
        """Fetch rep records and calculate (sum) rep for the user"""
        rep_records = RepRecord.fetch_all(self.id)
        sum_ = sum([record.rep_value for record in rep_records])
        return sum_

    def add_to_group(self, group_title):
        group = Group(group_title)
        if group not in self.groups:
            self.groups.append(Group.fetch(group_title) or group)

    def last_vote(self, recipe_id):
        return DBSession.query(VoteRecord)\
                        .filter(VoteRecord.recipe_id == recipe_id)\
                        .filter(VoteRecord.user_id == self.id)\
                        .order_by(desc(VoteRecord.creation_time))\
                        .first()

    @property
    def display_name(self):
        """
        Return a display name.
        Fallback to email if the user has no profile
        """
        display_name = self.email
        if self.profile:
            display_name = self.profile.nickname or self.profile.real_name
        return display_name

    def gravatar_url(self, size=20):
        default = 'identicon'
        url = 'http://www.gravatar.com/avatar/%s?%s' %\
              (md5(self.email).hexdigest(),
               urlencode({'d': default, 's': str(size)}))
        return url

    @classmethod
    def fetch(cls, id_=None, email=None):
        query = DBSession.query(cls)
        if id_:
            return query.get(id_)
        elif email:
            return query.filter(cls.email == email).first()
        return None

    @classmethod
    def multidict_to_dict(cls, multidict):
        return {'email': multidict.getone('email'),
                'password': multidict.getone('password')}

    @classmethod
    def construct_from_dict(cls, cstruct):
        """The way to construct new user"""
        user_schema = UserSchema()
        try:
            appstruct = user_schema.deserialize(cstruct)
        except Invalid, e:
            return {'errors': e.asdict(),
                    'original_data': cstruct}
        id_ = generate_id()
        hash_ = generate_hash(appstruct['password'])
        groups = [Group('applied')]
        user = cls(id_, appstruct['email'], hash_, groups)
        return user

    @classmethod
    def user_groups(cls, user_id, request):
        """
        The callback function for AuthTktAuthenticationPolicy
        """
        group_titles = None
        from kook import caching
        user = caching.get_user(user_id)
        if user:
            group_titles = []
            for group in user.groups:
                group_titles.append(group.title)
        return group_titles

    @classmethod
    def fetch_all(cls, limit=10):
        users = DBSession.query(cls).limit(limit).all()
        return sorted(users, key=lambda user: user.profile.rep,
                      reverse=True)


class RepRecord(Entity):
    """A reputation record for a user"""
    def __init__(self, user_id, rep_value, subject, obj=None):
        self.user_id = user_id
        self.rep_value = rep_value
        self.subject = subject
        self.creation_time = datetime.now()
        try:
            self.object_id = obj.ID
        except AttributeError:
            self.object_id = None

    @classmethod
    def fetch(cls, user_id, subject=None, obj=None, latest=True):
        query = DBSession.query(cls)
        if subject:
            query = query.filter(cls.subject == subject)
        if obj:
            query = query.filter(cls.object_id == obj.ID)
        if latest:
            return query.filter(cls.user_id == user_id)\
                        .order_by(desc(cls.creation_time))\
                        .first()
        return None

    @classmethod
    def fetch_all(cls, user_id):
        """Fetch all rep records for a user"""
        query = DBSession.query(cls).filter(cls.user_id == user_id).all()
        return query


#========
# MAPPERS
#========

from kook.models.recipe import VoteRecord, Dish

mapper(User, users,
       properties={
           'groups': relationship(Group, secondary=user_groups, lazy='joined'),
           'favourite_dishes': relationship(Dish, secondary=user_favourites),
           'rep_records': relationship(RepRecord, lazy='joined'),
           'profile': relationship(Profile, uselist=False, lazy='joined',
                                   cascade='all, delete, delete-orphan')})

mapper(Group, groups)
mapper(Profile, profiles)
mapper(RepRecord, rep_records)