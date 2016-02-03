import webapp2
import json

from google.appengine.ext import ndb

class UserAndroid(ndb.Model):
    email = ndb.StringProperty()
    android_token = ndb.StringProperty()
    is_logged = ndb.BooleanProperty()
    language = ndb.StringProperty()
    
    @classmethod
    def queryUser(cls, myEmail, myAndroidToken):
        #return 1
        return cls.query(cls.email == myEmail, cls.android_token == myAndroidToken)

class userAndroidController(webapp2.RequestHandler):
    
    def login(self):
        myEmail = self.request.get('email')
        myAndroidToken = self.request.get('android_token')
        myLanguage = self.request.get('language')
        if self.userExists(myEmail, myAndroidToken) == True:
            users = UserAndroid.queryUser(myEmail, myAndroidToken)
            self.update(users, True, myLanguage)
        else:
            self.create(myEmail, myAndroidToken, myLanguage)
            
    def logout(self):
        myEmail = self.request.get('email')
        myAndroidToken = self.request.get('android_token')
        myLanguage = self.request.get('language') 
        users = UserAndroid.queryUser(myEmail, myAndroidToken)       
        self.update(users, False, myLanguage)
            
        
        #return False
    
    def create(self, myEmail, myAndroidToken, myLanguage):
        try:
            user = UserAndroid(email = myEmail, android_token = myAndroidToken, is_logged = True, language = myLanguage)
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
            
        
    def userExists(self, myEmail, myAndroidToken):
        users = UserAndroid.queryUser(myEmail, myAndroidToken)
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
            users = UserAndroid.queryUser(myEmail, myUdid)
            for user in users:
                user.language = myLanguage
                user.put()
                self.successResponse()
        
        
        
         