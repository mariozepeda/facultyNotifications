import webapp2
import ssl
import json
import socket
import struct
import binascii

class NotificationController(webapp2.RequestHandler):


	def test(self):


		TOKEN = '658137ada8f7c16584353241e9a7dfd867b54940a3eda8b263a7a12882d99df0'
		PAYLOAD = {
		    'aps': {
		        'alert': 'Test Faculty',
		        'sound': 'default'
		    }
		}
		PASSPHRASE = 'pushchat'

		self.send_push(TOKEN,json.dumps(PAYLOAD))

		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('finished')


	def send_push(self,token, payload):
	    # Your certificate file
	    cert = 'ck.pem'
	    key = 'newFacultyKey.pem'
	    passphrase = 'Q1w2e3r4t5@'
	    host = 'gateway.sandbox.push.apple.com';
	    host_ip = socket.gethostbyname( host )

	    try:

		    # APNS development server
		    apns_address = (host_ip, 2195)

		    # Use a socket to connect to APNS over SSL
		    s = socket.socket()
		    sock = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv3, certfile=cert, keyfile=key )
		    sock.connect(apns_address)

		    # Generate a notification packet
		    token = binascii.unhexlify(token)
		    fmt = '!cH32sH{0:d}s'.format(len(payload))
		    cmd = '\x00'
		    message = struct.pack(fmt, cmd, len(token), token, len(payload), payload)
		    sock.write(message)
		    sock.close()

	    except Exception, e:
	    	self.response.write("Something's wrong with %s. Exception type is %s" % (apns_address, e))