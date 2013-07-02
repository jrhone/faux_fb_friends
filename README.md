faux_fb_friends
===============
PROGRAMMING EXERCISE
--------------------

For this exercise you will be building a web app to serve as the backend API for an imaginary iOS/Android application. The web app should accomplish the tasks in the list below. It should be written in Python/Django, and should be deployed to the Heroku account we've assigned you. It should use MongoDB for storage. Feel free to use (or don't use) any of the other add-ons in the Heroku account.

We have provided a fake Facebook service for getting a list of a user's friends. The service provides a list of fake friends for a 'user' based on an email address. The service is deterministic with regard to the output for a given email address, but otherwise the data is random. You should expect that there will be overlap between friends for different users/email addresses.

Here is a link to a mongo.Person python file that describes the data model to be used in your example web app. This model was written using the ORM library MongoEngine. You are NOT required to integrate this model with Django's standard ORM, trying to do so may actually complicate things for you; but if you prefer, feel free to try. ;-)

Your work will be judged primarily based on functional completeness as well as the efficiency/responsiveness of the endpoints. We aren't looking for any minimum bar of performance, nor will we be measuring milliseconds; we're more interested in how different techniques/approaches can affect responsiveness/efficiency. So while you're not required to make the endpoints as responsive as possible, you should be prepared to discuss the performance implications of the implementation and what additional changes could be made to improve performance.

Create a 'Registration' endpoint that allows a user to "register", accepting and populating the fields on the mongo.Person object. 

Registration should take care of the following items:
- Create a Person record in mongodb for the user based on data submitted to the endpoint
- Retreives all of the user's friends from the faux-facebook 'friends list' service. NOTE: This service was written to simulate random latency that can occur when depending on an external service like FB
- Creates a Person record for each friend
- The response for the endpoint should be the json respresentation of the user
- Send a 'succesful registration' email once the user's registration is complete

Create a 'Show Friends' endpoint that expects an email address returns a json array of all the user's friends in the same format as the singular mongo.Person.to_json() method. In our imaginary app, this endpoint will be called frequently, so some thought should be given to performance.


SOLUTION:

See code implementation.  Specifically:
- codingexercise/models.py
- codingexercise/views.py
- hingetest/urls.py


SCRATCH NOTES:

# Test register endpoint
curl -X POST --header "Content-Type:application/json" -d "email=j@gmail.com&first_name=j&last_name=r&gender=M&city=Jamaica" http://hinge-interview02.herokuapp.com/register | python -mjson.tool

# Test friends endpoint
curl -X POST --header "Content-Type:application/json" -d "email=j@gmail.com" http://hinge-interview02.herokuapp.com/friends | python -mjson.tool

# Connect to Mongo DB
mongo -u heroku_app14429742 -p b0ohnarudeiq335nudjnvvfsf5 ds041337.mongolab.com:41337/heroku_app14429742


tradeoffs analysis
  run through code
    minimized mongo calls
    batch writes/reads
  memcache for friends endpoint
    write to the cache after calling fb_get_friends
    or
    invalidate cache after calling fb_get_friends
    write to cache on read
  pagination for friends endpoint
        

foreman start
