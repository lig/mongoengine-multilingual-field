from mongoengine import Document

from multilingual_field.fields import MultilingualStringField


class TestDocument(Document):
    name = MultilingualStringField()
