from rest_framework.exceptions import ValidationError


# class LinkValidator:
#
#     def __init__(self, field):
#         self.field = field
#
#     def __call__(self, value):
#         youtube = 'www.youtube.com'
#         tmp_value = dict(value).get(self.field)
#         if not bool(youtube in tmp_value.lower()):
#             raise ValidationError('Ссылка курса или урока должна быть на Youtube')


def link_validator(value):
    youtube = 'www.youtube.com'
    if not bool(youtube in value.lower()):
        raise ValidationError('Ссылка курса или урока должна быть на Youtube')
