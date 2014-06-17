from twisted.internet import kqreactor
kqreactor.install()

from twisted.internet import reactor, protocol, endpoints, defer
from twisted.enterprise import adbapi


dbpool = adbapi.ConnectionPool("MySQLdb", host='localhost', db='yunwei', user='yunwei', passwd='yunwei')


class CustomProtocol(protocol.Protocol):
	
	def connectionMade(self):
		self.transport.write('checking db now...\r\n')
		d = self.getEmailFromDB()
		d.addCallback(self.filterResult)
		d.addCallback(self.transport.write)
		d.addCallback(self.transport.loseConnection)

	def getEmailFromDB(self):
		return dbpool.runQuery("select email from auth_user where id=1")

	def filterResult(self, r):
		if r:
			for user in r:
				for email in user:
					return email
		return 'no data returned'




def main():
	factory = protocol.ServerFactory()
	factory.protocol = CustomProtocol
	endpoints.serverFromString(reactor, "tcp:1234").listen(factory)
	reactor.run()

if __name__ == '__main__':
    main()



