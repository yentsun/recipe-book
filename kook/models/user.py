import cryptacular.bcrypt
from hashlib import md5
from urllib import urlencode
from datetime import date
from colander import Invalid
from kook.models import Entity, DBSession
from schemas import UserSchema, ProfileSchema, dont_check_current_nickname

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

class Group(Entity):

    def __init__(self, title):
        self.title = title

class User(Entity):

    def __init__(self, id, email, password_hash, groups=None, profile=None,
                 favourite_titles=None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.groups = groups or []
        self.profile = profile or Profile()
        self.favourite_titles = favourite_titles or []

    def check_password(self, password):
        return crypt.check(self.password_hash, password)

    def generate_password(self):
        """Generate new password and send it to user email"""
        #TODO complete function
        return '000000'

    @property
    def gravatar_url(self):
        default = 'identicon'
        size = 20
        url = 'http://www.gravatar.com/avatar/%s?%s' %\
              (md5(self.email).hexdigest(),
               urlencode({'d':default, 's':str(size)}))
        return url

    @classmethod
    def generate_hash(cls, password):
        return crypt.encode(password)

    @classmethod
    def fetch(cls, id=None, email=None):
        query = DBSession.query(cls)
        if id:
            return query.get(id)
        elif email:
            return query.filter(cls.email==email).first()
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
        id = cls.generate_id()
        hash = cls.generate_hash(appstruct['password'])
        groups = [Group('applied')]
        user = cls(id, appstruct['email'], hash, groups)
        return user

    @classmethod
    def group_finder(cls, id=None, request=None, user=None):
        """
        The callback function for AuthTktAuthenticationPolicy
        """
        if user:
            user = user
        elif id:
            user = DBSession.query(cls).get(id)
        else:
            return None
        groups = user.groups
        strings = []
        for instance in groups:
            strings.append(instance.title)
        return strings

class Profile(Entity):
    """Profile for a user"""

    def __init__(self, nickname=None, real_name=None, birthday=None,
                 location=None, registration_day=None):
        self.nickname = nickname
        self.real_name = real_name
        self.birthday = birthday
        self.location = location
        self.registration_day = registration_day or date.today()

    @classmethod
    def fetch(cls, nickname):
        query = DBSession.query(cls)
        return query.filter(cls.nickname==nickname).first()

    @classmethod
    def construct_from_multidict(cls, multidict, **kwargs):
        current_profile=kwargs.get('current_profile')
        skip_nickname = False
        if current_profile.nickname == multidict.getone('nickname'):
            skip_nickname = True
        schema = ProfileSchema(after_bind=dont_check_current_nickname)\
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