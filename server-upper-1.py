from twisted.internet import kqreactor
kqreactor.install()

from twisted.internet import reactor, protocol, endpoints


class UpperProtocol(protocol.Protocol):
	client_name = ''

	def connectionLost(self, r):
		print "bye, client %s" % self.client_name

	def dataReceived(self, data):
		self.client_name = data
		self.transport.write(data.upper())
		#self.transport.loseConnection()




def main():
	factory = protocol.ServerFactory()
	factory.protocol = UpperProtocol

	endpoints.serverFromString(reactor, "tcp:1234").listen(factory)
	reactor.run()

if __name__ == '__main__':
    main()



