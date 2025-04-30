import json


class JSONBaseBuilder:

    def __init__(self):
        self.fields = {}

    def id(self, id):
        self.fields['id'] = id
        return self

    def build(self):
        return self.fields


class JSONClientBuilder(JSONBaseBuilder):

    def name(self, name):
        self.fields['name'] = name
        return self

    def email(self, email):
        self.fields['email'] = email
        return self