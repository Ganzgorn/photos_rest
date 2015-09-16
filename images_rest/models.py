from django.db.models import *
from django.forms.models import model_to_dict


GENDER_CHOICES = (
    ('М', 'Муж.'),
    ('Ж', 'Жен.'),
)


TYPES = (
    ('jpg', 'JPEG'),
    ('gif', 'GIF'),
    ('png', 'PNG')
)


class User(Model):
    username = CharField(max_length=255, unique=True)
    firstname = CharField(max_length=50, blank=True)
    lastname = CharField(max_length=50, blank=True)
    gender = CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    email = CharField(max_length=255, blank=True)
    created = DateTimeField(auto_now=True)


class Photo(Model):

    name = CharField(max_length=255, blank=True)
    path = CharField(max_length=1024)
    url = CharField(max_length=512)
    border_color = CharField(max_length=20, default='000000')
    alpha = CharField(max_length=5, blank=True)
    type = CharField(max_length=3, choices=TYPES, default='jpg')
    date = DateTimeField(auto_now=True)
    user = ForeignKey(User)

    def get_dict(self):
        result = model_to_dict(self, fields=['name', 'path', 'url', 'border_color', 'alpha', 'type'], exclude=[])
        result['user'] = self.user.username
        result['date'] = self.date.strftime('%Y-%m-%d %H:%M:%S')
        return result