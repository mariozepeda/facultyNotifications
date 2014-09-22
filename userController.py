import webapp2
import json

from google.appengine.ext import ndb

class User(ndb.Model):
    email = ndb.StringProperty()
    udid = ndb.StringProperty()
    is_logged = ndb.BooleanProperty()
    
    @classmethod
    def queryUser(cls, myEmail, myUdid):
        #return 1
        return cls.query(cls.email == myEmail, cls.udid == myUdid)

class userController(webapp2.RequestHandler):
    
    def login(self):
        return False
    
    def create(self):        
        #myEmail = ndb.Key("email","mmzepedab@gmail.com")
        users = User.queryUser("oscar.espirilla@gmail.com", "669")
        if users.count() > 0:
            for user in users:
                user.udid = "667"
                user.put()
                #self.response.out.write('<blockquote>%s</blockquote>' % user.udid)
            #self.response.out.write('Se ha actualizado %s registro(s)' % users.count())
        else:
            user = User(email = self.request.get('email'), udid = self.request.get('udid'), is_logged = True)
            user.put()
        
        
        #self.response.write('</br></br>User create succesfully')

        self.response.headers['Content-Type'] = 'application/json'   
        obj = {
                'success': True, 
                'payload': 'some var',
                } 
        self.response.out.write(json.dumps(obj))