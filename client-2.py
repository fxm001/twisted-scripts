

from twisted.internet import reactor, protocol, endpoints, defer
import sys


class UpperClientProtocol(protocol.Protocol):
	
	def connectionMade(self):
		self.transport.write(self.factory.text + '\r\n')

	def dataReceived(self, data):
		self.factory.deferred.callback(data)
		#self.transport.loseConnection()


class UpperClientFactory(protocol.ClientFactory):
	text = ''
		


def gotData(data):
	print "response data is:", data


def allDone(results):
	reactor.stop()

if __name__ == '__main__':

	# get data from commandline
	port = sys.argv[1]
	data_to_send = sys.argv[2:]
	endpoint = endpoints.clientFromString(reactor, "tcp:127.0.0.1:%s" % port)

	all_deferreds = []
	for data in data_to_send:
		print 'sending', data
		d = defer.Deferred()
		d.addCallback(gotData)
		factory = UpperClientFactory()
		factory.protocol = UpperClientProtocol
		factory.text = data
		factory.deferred = d
		all_deferreds.append(d)
		endpoint.connect(factory)

	deferredList = defer.DeferredList(all_deferreds)
	deferredList.addCallback(allDone)
	
	reactor.run()



