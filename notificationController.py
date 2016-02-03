import webapp2
import json
import ssl
import json
import socket
import struct
import binascii
import urllib2

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
    
    @classmethod
    def queryUserByEmail(cls, myEmail):
        #return 1
        return cls.query(cls.email == myEmail)

class UserAndroid(ndb.Model):
    email = ndb.StringProperty()
    android_token = ndb.StringProperty()
    is_logged = ndb.BooleanProperty()
    language = ndb.StringProperty()
    
    @classmethod
    def queryUser(cls, myEmail, myAndroidToken):
        #return 1
        return cls.query(cls.email == myEmail, cls.android_token == myAndroidToken)
    
    @classmethod
    def queryUserByEmail(cls, myEmail):
        #return 1
        return cls.query(cls.email == myEmail)

class NotificationController(webapp2.RequestHandler):
    
    def sendNotification(self):
        myEmail = self.request.get('email')
        myType = self.request.get('type')
        myCourseName = self.request.get('courseName')
        users = User.queryUserByEmail(myEmail)
        usersAndroid = UserAndroid.queryUserByEmail(myEmail)
        
        for user in users:               
            if user.is_logged == True:
                #token = '658137ada8f7c16584353241e9a7dfd867b54940a3eda8b263a7a12882d99df0'
                token = user.udid
                
                notificationText = self.getNotificationText(myType,myCourseName,user.language)
                
                payload = {'aps': {'alert': notificationText,'sound': 'default'}}
                payload = json.dumps(payload)
                cert = 'ck.pem'
                key = 'newFacultyKey.pem'
                host = 'gateway.push.apple.com';
                host_ip = socket.gethostbyname( host )
    
                try:
                    # APNS development server
                    apns_address = (host_ip, 2195)
        
                    # Use a socket to connect to APNS over SSL
                    s = socket.socket()
                    sock = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv23, certfile=cert, keyfile=key )
                    sock.connect(apns_address)
        
                    # Generate a notification packet
                    token = binascii.unhexlify(token)
                    fmt = '!cH32sH{0:d}s'.format(len(payload))
                    cmd = '\x00'
                    message = struct.pack(fmt, cmd, len(token), token, len(payload), payload)
                    sock.write(message)
                    sock.close()
                    
                except Exception, e:
                    self.response.write("Wrong %s. Exception type is %s" % (apns_address, e))

        for userAndroid in usersAndroid:
            #self.response.out.write("Huh?") 
            if userAndroid.is_logged == True:
                #token = '658137ada8f7c16584353241e9a7dfd867b54940a3eda8b263a7a12882d99df0'
                token = userAndroid.android_token
                
                notificationText = self.getNotificationText(myType,myCourseName,userAndroid.language)
                
                json_data = {"collapse_key" : "msg","data" : { "data": notificationText, }, "registration_ids": [token],}

                url = 'https://android.googleapis.com/gcm/send'
                myKey = "AIzaSyA3XNF4chKCR9s19pJaEttuLIQBoDNO150" 
                data = json.dumps(json_data)
                headers = {'Content-Type': 'application/json', 'Authorization': 'key=%s' % myKey}
                req = urllib2.Request(url, data, headers)
                f = urllib2.urlopen(req)
                response = json.loads(f.read())

                self.response.out.write(json.dumps(response,sort_keys=True, indent=2) )                
            
                
    def userIsLoggedIn(self, myEmail):
        return True
    
    def getNotificationText(self, myType, myCourseName, myLanguage):
        #SPANISH NOTIFICATION TEXT
        if myLanguage == "es":
            if myType == "9":
                return "Felicidades! Usted ha sido inscrito en el %s" % myCourseName
            elif myType == "10":
                text = "Su solicitud para %s ha sido recibida y esta pendiente de aprobacion." % myCourseName
                return unicode(text).encode('utf-8')
            elif myType == "11":
                return "%s esta a punto de comenzar Solo falta una semana!" % myCourseName
            elif myType == "12":
                return "%s esta a punto de terminar! !Solo una semana mas!" % myCourseName
            elif myType == "13":
                return "%s ha comenzado! Asegurese de unirse a nosotros!" % myCourseName
            elif myType == "14":
                return "%s ha terminado. Gracias por participar!" % myCourseName
            elif myType == "15":
                return "Ha pasado un tiempo desde que tomo parte en el %s Nos encantaria tenerlo de vuelta!" % myCourseName
            elif myType == "16":
                return "Ha pasado un tiempo desde que tomo parte en el %s Nos encantaria tenerlo de vuelta!" % myCourseName
            elif myType == "17":
                return "Su solicitud de retirarse del %s ha sido procesada." % myCourseName
            elif myType == "18":
                return "Lo sentimos, su solicitud para participar en el %s ha sido denegada." % myCourseName
            elif myType == "19":
                return "Se ha cancelado su solicitud de inscripcion al curso  %s" % myCourseName
            elif myType == "20":
                return "Su solicitud de retirarse del curso %s ha sido procesada." % myCourseName
        #ENGLISH NOTIFICATION TEXT    
        elif myLanguage == "en":
            if myType == "9":
                return "Congratulations! You have been enrolled into the %s" % myCourseName
            elif myType == "10":
                return "Your request for %s has been received and is pending approval" % myCourseName
            elif myType == "11":
                return "%s is about to start! Only one week away!" % myCourseName
            elif myType == "12":
                return "%s is almost over! Only one more week left!" % myCourseName
            elif myType == "13":
                return "%s has begun! Be sure to join us!" % myCourseName
            elif myType == "14":
                return "%s has ended. Thank you for participating!" % myCourseName
            elif myType == "15":
                return "It's been a while since you took part in the %s We'd love to have you back!" % myCourseName
            elif myType == "16":
                return "It's been a while since you took part in the %s We'd love to have you back!" % myCourseName
            elif myType == "17":
                return "Your request to withdraw from the %s has been processed." % myCourseName
            elif myType == "18":
                return "We're sorry, your request to join the %s has been denied." % myCourseName
            elif myType == "19":
                return "Your request for the %s  course has been canceled." % myCourseName
            elif myType == "20":
                return "Your request to withdraw from the %s course has been processed." % myCourseName
        #PORTUGUESE NOTIFICATION TEXT    
        elif myLanguage == "pt":
            if myType == "9":
                return "Parabens! Voce ja esta inscrito no curso %s" % myCourseName
            elif myType == "10":
                return "O seu pedido foi recebido e esta pendente de aprovacao %s" % myCourseName
            elif myType == "11":
                return "%s ja vai comecar! Em apenas uma semana!" % myCourseName
            elif myType == "12":
                return "%s ja vai comecar! Em apenas uma semana!" % myCourseName
            elif myType == "13":
                return "%s ja comecou! Certifique se de se juntar a nos!" % myCourseName
            elif myType == "14":
                return "%s terminou. Obrigado por participar!" % myCourseName
            elif myType == "15":
                return "Ja faz um tempo desde que voce participou do %s Adorariamos ter voce de volta!" % myCourseName
            elif myType == "16":
                return "Ja faz um tempo desde que voce participou do %s Adorariamos ter voce de volta!" % myCourseName
            elif myType == "17":
                return "Sua solicitacao para retirar se do %s foi processada." % myCourseName
            elif myType == "18":
                return "Sentimos muito, sua solicitacao para entrar no %s foi negada<" % myCourseName
            elif myType == "19":
                return "Sua inscricao no curso  %s  foi cancelada." % myCourseName
            elif myType == "20":
                return "Sua solicitacao para retirar se do curso %s foi processada." % myCourseName
        
        
    
    
        
        
        
         