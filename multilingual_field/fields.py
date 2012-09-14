from collections import Mapping

from i18n_string import MultilingualString
from mongoengine.base import BaseField


def _translate(self, language):

    for field_name, field in self._fields.items():

        if isinstance(field, MultilingualStringField):
            value = getattr(self, field_name)
            setattr(self, field_name, value.translate(language))


class MultilingualStringField(BaseField):

    def to_mongo(self, value):
        return [{'lang': k, 'value': v} for k, v in value.translations.items()]

    def to_python(self, value):
        return MultilingualString(
            {item['lang']: item['value'] for item in value})

    def __set__(self, instance, value):

        if not isinstance(value, MultilingualString):

            if isinstance(value, Mapping):
                value = MultilingualString(value)
            elif isinstance(value, basestring):
                old_value = instance._data.get('name')

                if old_value:
                    old_value.translations[old_value.language] = value
                    value = old_value

        super(MultilingualStringField, self).__set__(instance, value)

    def __get__(self, instance, owner):

        if not hasattr(instance, 'translate'):
            owner.translate = _translate

        return super(MultilingualStringField, self).__get__(instance, owner)
