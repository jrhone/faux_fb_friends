# -*- coding: utf-8 -*-
import datetime
import mongoengine


class City(mongoengine.Document):
    """
    This models represents a city
    """
    location_name = mongoengine.StringField()
    created_dts = mongoengine.DateTimeField(default=datetime.datetime.now)

    def to_string(self):
        return self.location_name


class Person(mongoengine.Document):
    """
    This models represents a user in the application
    """
    email = mongoengine.EmailField(primary_key=True)

    first_name = mongoengine.StringField(required=True)
    last_name = mongoengine.StringField(required=True)
    age = mongoengine.IntField()

    #male vs female
    gender = mongoengine.StringField(choices=["M","F"], required=True)

    #if a city doesn't exist for a person, create it, then assign it to the person
    city = mongoengine.ReferenceField(City)

    #single vs taken
    relationship_status = mongoengine.StringField(choices=["S","T"])

    created_dts = mongoengine.DateTimeField(default=datetime.datetime.now)
    date_joined = mongoengine.DateTimeField()

    #list of all friends' emails
    friends = mongoengine.ListField(mongoengine.StringField())

    def to_json(self):
        # dereference city 
        data = self._data
        city = self.city

        data['city'] = city.to_string()
        return data
