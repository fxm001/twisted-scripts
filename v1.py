from twisted.internet import kqreactor
kqreactor.install()

from twisted.internet import reactor, protocol


factory = protocol.ServerFactory()
factory.protocol = protocol.Protocol

reactor.listenTCP(8000, factory)
print reactor.mainLoop
reactor.run()

