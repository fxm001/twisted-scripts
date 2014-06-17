from twisted.internet import kqreactor
kqreactor.install()

from twisted.internet import reactor, protocol, endpoints
from twisted.protocols.basic import LineReceiver

import urllib2
import time


class ProxyProtocol(LineReceiver):

	def lineReceived(self, line):
		start = time.time()
		print "feteching", line
		# urllib2 is blocking code
		data = urllib2.urlopen(line).read()
		print "fetched", line
		self.transport.write(data)
		self.transport.loseConnection()
		print "took", time.time() - start		



def main():
	factory = protocol.ServerFactory()
	factory.protocol = ProxyProtocol
	endpoints.serverFromString(reactor, "tcp:1234").listen(factory)
	reactor.run()

if __name__ == '__main__':
    main()



