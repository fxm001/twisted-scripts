from twisted.internet import kqreactor
kqreactor.install()

from twisted.internet import reactor, protocol, endpoints


class UpperProtocol(protocol.Protocol):
	
	def connectionMade(self):
		#self.transport.write('hi there, welcome\n')
		pass

	def connectionLost(self, r):
		print "client disconnected."

	def dataReceived(self, data):
		self.transport.write(data.upper())
		#self.transport.loseConnection()




def main():
	factory = protocol.ServerFactory()
	factory.protocol = UpperProtocol

	endpoints.serverFromString(reactor, "tcp:1234").listen(factory)
	reactor.run()

if __name__ == '__main__':
    main()



