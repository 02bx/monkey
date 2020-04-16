"""
Define a Document Schema for the Monkey document.
"""
from mongoengine import Document, StringField, DateTimeField


class TestTelem(Document):
    # SCHEMA
    name = StringField(required=True)
    time = DateTimeField(required=True)
    method = StringField(required=True)
    endpoint = StringField(required=True)
    content = StringField(required=True)
