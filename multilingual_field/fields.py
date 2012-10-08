from collections import Mapping

from mongoengine.fields import DictField


def _translate(self, language):

    for field_name, field in self._fields.items():

        if isinstance(field, MultilingualStringField):
            value = getattr(self, field_name)
            setattr(self, field_name, value.translate(language))


class MultilingualStringField(DictField):

    def to_mongo(self, value):
        if not isinstance(value, Mapping):
            return value
        return [{'lang': k, 'value': v} for k, v in value.items()]

    def to_python(self, value):
        return {item['lang']: item['value'] for item in value}

    def lookup_member(self, member_name):
        return member_name != 'S' and member_name or None
