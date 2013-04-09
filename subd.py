#!/usr/bin/env python
import sys, time, signal
import daemon
import demonconfig

StaticConfig = demonconfig.StatCon()

class MyDaemon(daemon.Daemon):
	def run(self):
		StaticConfig.run()
 
class DaemonConfigurator:
	
	def __init__(self,ourdaemon):
		self.ourdaemon = ourdaemon
	
	def GetSignalsForDaemon(self):
		localCon = demonconfig.SigFunctionsCon(self.ourdaemon)
		SigDict={}
		for Sig in dir(localCon):
			if Sig[0:1]!='_':
				SigDict[getattr(signal, Sig)]=getattr(localCon, Sig)
		return SigDict
		
	def GetReactsForDaemon(self):
		localCon = demonconfig.ReactFunctionCon(self.ourdaemon)
		ReactDict={}
		for React in dir(localCon):
			if React[0:1]!='_':
				ReactDict[React]=getattr(localCon, React)
		return ReactDict


if __name__ == "__main__":
	
	daemon = MyDaemon(StaticConfig.PidFile, StaticConfig.Inputter, StaticConfig.Outputter, StaticConfig.Errorer)
	
	configer = DaemonConfigurator(daemon)
	SigDict = configer.GetSignalsForDaemon()
	
	daemon.MetaInit(SigDict)
	
	ReactDict = configer.GetReactsForDaemon()
	
	print len(sys.argv)
	if len(sys.argv) > 1:
		if sys.argv[1] in iter(ReactDict):
			try:
				ReactDict[sys.argv[1]](*sys.argv[2:len(sys.argv)])
				sys.exit(0)
			except TypeError, error:
				print error
				print StaticConfig.Help
				sys.exit(2)
		else:
			print "usage: %s %s" % sys.argv[0] % str(self.ReactDict)
			sys.exit(2)
