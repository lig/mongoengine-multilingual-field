from i18n_string import MultilingualString
from mongoengine.base import BaseField


class MultilingualStringField(BaseField):

    def to_mongo(self, value):
        return [{'lang': k, 'value': v} for k, v in value.translations.items()]

    def to_python(self, value):
        return MultilingualString(
            {item['lang']: item['value'] for item in value})

    def __set__(self, instance, value):

        if not isinstance(value, MultilingualString):
            value = MultilingualString(value)

        super(MultilingualStringField, self).__set__(instance, value)

    def __get__(self, instance, owner):
        value = super(MultilingualStringField, self).__get__()
        return BaseField.__get__(self, instance, owner)
