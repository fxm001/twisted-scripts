from twisted.internet import kqreactor
kqreactor.install()

from twisted.internet import reactor, protocol, endpoints, defer
from twisted.protocols.basic import LineReceiver
from twisted.web.client import getPage



class CachingProxyProtocol(LineReceiver):

	def _getPage(self, url):
		""" always return Deferred object here"""
		try:
			data = self.factory.cache[url]
			return defer.succeed(data)
		except KeyError:
			d = getPage(url)
			d.addCallback(self._storeInCache, url, self.factory.cache)
			return d

	def _storeInCache(self, data, url, cache):
		cache[url] = data
		return data

	def writeData(self, data):
		self.transport.write(data)
		self.transport.loseConnection()
	
	def lineReceived(self, line):
		d = self._getPage(line)
		d.addCallback(self.writeData)
	

class CachingProxyFactory(protocol.ServerFactory):
	protocol = CachingProxyProtocol
	cache = {}
						



def main():
	factory = CachingProxyFactory()
	endpoints.serverFromString(reactor, "tcp:1234").listen(factory)
	reactor.run()

if __name__ == '__main__':
    main()



