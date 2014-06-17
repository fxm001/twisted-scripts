

from twisted.internet import reactor, protocol, endpoints
import sys


class UpperClientProtocol(protocol.Protocol):
	
	def connectionMade(self):
		self.transport.write(self.factory.text + '\r\n')

	def dataReceived(self, data):
		print data
		#self.transport.loseConnection()


class UpperClientFactory(protocol.ClientFactory):
	text = ''
		


if __name__ == '__main__':

	# get data from commandline
	port = sys.argv[1]
	data_to_send = sys.argv[2:]
	endpoint = endpoints.clientFromString(reactor, "tcp:127.0.0.1:%s" % port)

	for data in data_to_send:
		print 'sending', data
		factory = UpperClientFactory()
		factory.protocol = UpperClientProtocol
		factory.text = data
		endpoint.connect(factory)
	
	reactor.run()



