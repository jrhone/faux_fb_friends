import datetime
import simplejson as json
from bson import json_util
import requests
import sys, traceback

from mongoengine.base import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseServerError
from codingexercise.models import City, Person

def add_friends(person):
    r = requests.get('http://faux-facebook.herokuapp.com/friends/?email=%s' % person.email)

    if r.status_code != 200:
        raise Exception('ffb friends list request failed')

    # get all friend emails    
    friend_data = r.json()['data']
    emails = [friend['email'] for friend in friend_data]
    
    # get friend emails in db
    existing_friends = Person.objects(email__in=emails).only('email')

    # batch insert missing friends
    s = set([friend.email for friend in existing_friends])
    people = [add_friend(friend) for friend in friend_data if friend['email'] not in s]

    if len(people) > 0:
        Person.objects.insert(people, write_options={'w':1})

    return emails


def add_friend(data):    
    try:
        # transform data for insert
        del data['id']
        data['first_name'] = data['name'].split(' ')[0]
        data['last_name'] = data['name'].split(' ')[1]

        if data.get('relationship status') and data['relationship status'] != '':
            data['relationship_status'] = data['relationship status']

        city, created = City.objects.get_or_create(location_name=data['city'], defaults={}, write_options={'w': 1})
        data['city'] = city #._data.get(None)

        #validate, dont save
        person = Person(**data)
        person.validate()

        return person
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        raise e


def register(request):
    if request.method == 'POST':
        try:
            user = request.POST.dict()
            
            try:
                # check existence before create
                people = Person.objects(email=user.get('email'))
                if people.count() > 0:
                    person = people[0]
                else:
                    city, created = City.objects.get_or_create(location_name=user.get('city'), defaults={}, write_options={'w': 1})            
                    user['city'] = city #._data.get(None)

                    person = Person(**user)
                    person.validate()

                # detect first registration
                if not person.date_joined:
                    person.date_joined = datetime.datetime.now()
                    person.friends = add_friends(person)
                    person.save(write_options={'w': 1})

                    send_mail('Registration Complete', 'Registration Successful!', 'rhone.j@gmail.com', [person.email], fail_silently=True)
            except ValidationError as err:
                return HttpResponseBadRequest(err)

            return HttpResponse(json.dumps(person.to_json(), default=json_util.default), content_type="application/json")
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return HttpResponseServerError()

    if request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])


def friends(request):    
    if request.method == 'POST':
        try:
            # get email list of friends
            friends_json = []
            user = Person.objects(email=request.POST['email']).only('friends').first()

            # match to friend objects in db
            if user:
                friends = Person.objects(email__in=user.friends)
                friends_json = [friend.to_json() for friend in friends]

            return HttpResponse(json.dumps(friends_json, default=json_util.default), content_type="application/json")
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return HttpResponseServerError()

    if request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])            


def index(request):
    return HttpResponse('alive')