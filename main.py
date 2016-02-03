#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
import urllib2
from notification_controller import NotificationController


class MainHandler(webapp2.RequestHandler):
    def get(self):
        #self.response.write('Hello world Again!')
        json_data = {"collapse_key" : "msg","data" : { "data": "Investigacion Academica esta a punto de finalizar", }, "registration_ids": ['dOVMGB6Kgn0:APA91bGj3PjzbupHOfNVbLgKiJ4uQJJKyo0b1A9zNm4tZsKXW5Uq-Ek5NXO894qVA9wZKTss5dm8v1abV_9o11YU-ca4PRbKyPyIzHPv3cRNAUwBsDOnFp2y2W0krcbSu_R4mSX-TO7i'],}

        url = 'https://android.googleapis.com/gcm/send'
        myKey = "AIzaSyA3XNF4chKCR9s19pJaEttuLIQBoDNO150" 
        data = json.dumps(json_data)
        headers = {'Content-Type': 'application/json', 'Authorization': 'key=%s' % myKey}
        req = urllib2.Request(url, data, headers)
        f = urllib2.urlopen(req)
        response = json.loads(f.read())


        self.response.out.write(json.dumps(response,sort_keys=True, indent=2) )   





app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/test', handler= 'notification_controller.NotificationController',  handler_method='test'),
    webapp2.Route('/user/create', handler= 'userController.userController',  handler_method='create'),
    webapp2.Route('/user/login', handler= 'userController.userController',  handler_method='login'),
    webapp2.Route('/user/loginAndroid', handler= 'userAndroidController.userAndroidController',  handler_method='login'),
    webapp2.Route('/user/logout', handler= 'userController.userController',  handler_method='logout'),
    webapp2.Route('/user/logoutAndroid', handler= 'userAndroidController.userAndroidController',  handler_method='logout'),
    webapp2.Route('/notification/send', handler= 'notificationController.NotificationController',  handler_method='sendNotification'),
    webapp2.Route('/user/changeLanguage', handler= 'userController.userController',  handler_method='changeLanguage'),
    webapp2.Route('/user/changeLanguageAndroid', handler= 'userAndroidController.userAndroidController',  handler_method='changeLanguage')
], debug=True)
