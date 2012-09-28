from mongoengine import Document

from multilingual_field.fields import MultilingualStringField


class TestDocument(Document):
    name1 = MultilingualStringField()
    name2 = MultilingualStringField()
