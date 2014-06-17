from twisted.internet import kqreactor
kqreactor.install()

from twisted.internet import reactor, protocol, endpoints


class UpperProtocol(protocol.Protocol):
	
	def connectionMade(self):
		self.factory.count += 1
		self.transport.write('hi there, welcome. now there is %d people online' % self.factory.count)

	def connectionLost(self, r):
		self.factory.count -= 1
		print "client disconnected."

	def dataReceived(self, data):
		self.transport.write(data.upper())
		#self.transport.loseConnection()


class CustomFactory(protocol.ServerFactory):
	count = 0




def main():
	factory = CustomFactory()
	factory.protocol = UpperProtocol
	endpoints.serverFromString(reactor, "tcp:1234").listen(factory)
	reactor.run()

if __name__ == '__main__':
    main()



