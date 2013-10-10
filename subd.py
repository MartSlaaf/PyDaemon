#!/usr/bin/env python
import sys
import time
import signal
import daemon
import demonconfig

StaticConfig = demonconfig.StatCon()

class MyDaemon(daemon.Daemon):
    
    
    def run(self):
        StaticConfig.run()
 
class DaemonConfigurator:
    
    
    def __init__(self,ourdaemon):
        self.ourdaemon = ourdaemon
    
    def getSignalsForDaemon(self):
        localCon = demonconfig.SigFunctionsCon(self.ourdaemon)
        sigDict={}
        for sig in dir(localCon):
            if sig[0:1]!='_':
                sigDict[getattr(signal, sig)]=getattr(localCon, sig)
        return sigDict
        
    def getReactsForDaemon(self):
        localCon = demonconfig.ReactFunctionCon(self.ourdaemon)
        reactDict={}
        for react in dir(localCon):
            if react[0:1]!='_':
                reactDict[react]=getattr(localCon, react)
        return reactDict


if __name__ == "__main__":
    
    daemon = MyDaemon(StaticConfig.pidFile, StaticConfig.inputter, StaticConfig.outputter, StaticConfig.errorer)
    
    configer = DaemonConfigurator(daemon)
    SigDict = configer.getSignalsForDaemon()
    
    daemon.metaInit(SigDict)
    
    ReactDict = configer.getReactsForDaemon()
    
    if len(sys.argv) > 1:
        if sys.argv[1] in iter(ReactDict):
            try:
                ReactDict[sys.argv[1]](*sys.argv[2:len(sys.argv)])
                sys.exit(0)
            except TypeError, error:
                print error
                print StaticConfig.strHelp
                sys.exit(2)
        else:
            print "usage: %s %s" % sys.argv[0] % ReactDict
            sys.exit(2)
