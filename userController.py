import webapp2
import json

from google.appengine.ext import ndb

class User(ndb.Model):
    email = ndb.StringProperty()
    udid = ndb.StringProperty()
    is_logged = ndb.BooleanProperty()
    language = ndb.StringProperty()
    
    @classmethod
    def queryUser(cls, myEmail, myUdid):
        #return 1
        return cls.query(cls.email == myEmail, cls.udid == myUdid)

class userController(webapp2.RequestHandler):
    
    def login(self):
        myEmail = self.request.get('email')
        myUdid = self.request.get('udid')
        myLanguage = self.request.get('language')
        if self.userExists(myEmail, myUdid) == True:
            users = User.queryUser(myEmail, myUdid)
            self.update(users, True, myLanguage)
        else:
            self.create(myEmail, myUdid, myLanguage)
            
    def logout(self):
        myEmail = self.request.get('email')
        myUdid = self.request.get('udid')
        myLanguage = self.request.get('language') 
        users = User.queryUser(myEmail, myUdid)       
        self.update(users, False, myLanguage)
            
        
        #return False
    
    def create(self, myEmail, myUdid, myLanguage):
        try:
            user = User(email = myEmail, udid = myUdid, is_logged = True, language = myLanguage)
            user.put()
            self.successResponse()
        except Exception, e:
            self.errorResponse(e)
            #self.response.write("Something's wrong with %s. Exception type is %s" % (apns_address, e))
                
        #myEmail = ndb.Key("email","mmzepedab@gmail.com")
        #users = User.queryUser(myEmail, myUdid)
        #if users.count() > 0:
            #for user in users:
                #if user.is_logged == True:
                    #user.is_logged = False
                #else:
                    #user.is_logged = True                
                #user.put()
                #self.response.out.write('<blockquote>%s</blockquote>' % user.udid)
            #self.response.out.write('Se ha actualizado %s registro(s)' % users.count())
        #else:
            #user = User(email = myEmail, udid = myUdid, is_logged = True)
            #user.put()        
        #self.response.write('</br></br>User create succesfully')

        
        
    def update(self, users, isLoggingIn, myLanguage):
        for user in users:
            if isLoggingIn:
                try:
                    user.is_logged = True
                    user.language = myLanguage
                    user.put()
                    self.successResponse()
                except Exception, e:
                    self.errorResponse(e)
            else:
                try:
                    user.is_logged = False
                    user.put()
                    self.successResponse()
                except Exception, e:
                    self.errorResponse(e)
            
        
    def userExists(self, myEmail, myUdid):
        users = User.queryUser(myEmail, myUdid)
        if users.count() > 0:
            return True
        else:
            return False
        
    def successResponse(self):
        self.response.headers['Content-Type'] = 'application/json'   
        obj = {
                'success': True, 
                #'payload': 'some var',
                } 
        self.response.out.write(json.dumps(obj))
        
    def errorResponse(self, error):
        self.response.headers['Content-Type'] = 'application/json'   
        obj = {
                'success': False, 
                'error': error,
                } 
        self.response.out.write(json.dumps(obj))
        
    def changeLanguage(self):
        myEmail = self.request.get('email')
        myUdid = self.request.get('udid')
        myLanguage = self.request.get('language')
        if self.userExists(myEmail, myUdid) == True:
            users = User.queryUser(myEmail, myUdid)
            for user in users:
                user.language = myLanguage
                user.put()
                self.successResponse()
        
        
        
         