#!/usr/bin/env python
import sys
import os
import imp

from twisted.internet import reactor
from bot import BotFactory, config_defaults

connections = {}

if __name__ == '__main__':
    if sys.version_info < (2, 5): 
        print >> sys.stderr, 'Error: Requires Python 2.5 or later, from www.python.org'
        sys.exit(1)
    
    pidfile = "spiffy.pid"

    try:
            pf = file(pidfile,'r')
            pid = pf.read().strip()
            try:
                pid = int(pid)
            except ValueError:
                pid = None
            pf.close()
    except IOError:
            pid = None

    if pid:
            print >> sys.stderr, "Pidfile (%s) already exists. Is spiffy already running?" % pidfile
            sys.exit(1)

    
    pid = os.getpid()
    file(pidfile,'w+').write("%s" % pid)

    config_name = os.path.join(sys.path[0], 'config.py')
    if not os.path.isfile(config_name):
        print >> sys.stderr, 'Error: No config(.py) file found.'
        sys.exit(1)

    config = imp.load_source('config', config_name)
    
    if hasattr(config, 'networks'):
        for network in config.networks:
            serverconfig = {}
            for x in config_defaults:
                serverconfig[x] = config_defaults[x]
            for x in config.__dict__:
                if not x.startswith('__'):
                    serverconfig[x] = config.__dict__[x]
            for x in config.networks[network]:
                serverconfig[x] = config.networks[network][x]
                
            serverconfig['network'] = network

            if 'host' not in serverconfig:
                print 'Error: Could not connect to %s. No host given.' % network
            else:
                print 'Creating connection to %s' % network
                server = serverconfig['host']
                port = 6667
                if isinstance(server, (tuple, list)):
                    server = server[0]
                
                ssl = False
                if ':' in server:
                    server, port = server.split(':')
                    if port.startswith('+'):
                        port = port[1:]
                        from twisted.internet import ssl
                        contextFactory = ssl.ClientContextFactory()
                        ssl = True
                    port = int(port)

                serverconfig['activeserver'] = (server, port or 6667)
                if ssl:
                    reactor.connectSSL(server, port or 6667, BotFactory(serverconfig, connections), contextFactory)
                else:
                    reactor.connectTCP(server, port or 6667, BotFactory(serverconfig, connections))
        reactor.run()
        if os.path.exists(pidfile):
            os.remove(pidfile)

    else:
        print >> sys.stderr, "Error: No networks to connect to."
        sys.exit(1)