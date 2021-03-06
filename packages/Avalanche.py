#!/usr/bin/env python
# Author P G Jones - 16/05/2012 <p.g.jones@qmul.ac.uk> : First revision
#        O Wasalski - 05/06/2012 <wasalski@berkeley.edu> : Added curl dependency
#        P G Jones - 11/07/2012 <p.g.jones@qmul.ac.uk> : Refactor into dev and fixed versions
# The AVALANCHE packages base class, allows for multiple avalanche versions
import LocalPackage
import os
import PackageUtil

class Avalanche( LocalPackage.LocalPackage ):
    """ Base avalanche installer for avalanche."""
    def __init__( self, name, zmqDependency, rootDependency, curlDependency ):
        """ Initialise avalanche with the tarName."""
        super( Avalanche, self ).__init__( name, False ) # Not graphical only
        self._ZeromqDependency = zmqDependency
        self._RootDependency = rootDependency
        self._CurlDependency = curlDependency
        return
    def GetDependencies( self ):
        """ Return the required dependencies."""
        return [self._ZeromqDependency, self._RootDependency, self._CurlDependency]
    def _IsInstalled( self ):
        """ Check if installed."""
        return PackageUtil.LibraryExists( os.path.join( self.GetInstallPath(), "lib/cpp" ), "libavalanche" )
    def _Install( self ):
        """ Install Avalanche."""
        env = os.environ
        env['PATH'] = os.path.join( self._DependencyPaths[self._RootDependency], "bin" ) + ":" + env['PATH']
        env['ROOTSYS'] = self._DependencyPaths[self._RootDependency]
        curl = self._DependencyPaths[self._CurlDependency] # Shorten the text
        zmq =  self._DependencyPaths[self._ZeromqDependency] # Shorten the text
        self._InstallPipe += PackageUtil.ExecuteSimpleCommand( "make", 
                                                               ['CXXFLAGS=-L%s/lib -I%s/include -L%s/lib -I%s/include' % (zmq, zmq, curl, curl) ],
                                                               env, 
                                                               os.path.join( self.GetInstallPath(), "lib/cpp" ) )
        return

class AvalancheRelease( Avalanche ):
    """ Base class for release versions."""
    def __init__( self, name, zmqDependency, rootDependency, curlDependency, tarName ):
        """ Initialise avalanche with the tarName."""
        super( AvalancheRelease, self ).__init__( name, zmqDependency, rootDependency, curlDependency )
        self._TarName = tarName
        return
    def _IsDownloaded( self ):
        """ Check if downloaded."""
        return os.path.exists( os.path.join( PackageUtil.kCachePath, self._TarName ) )
    def _Download( self ):
        """ Download avalanche (git clone)."""
        self._DownloadPipe += PackageUtil.DownloadFile( "https://github.com/mastbaum/avalanche/tarball/" + self._TarName )
        return
    def _Install( self ):
        """ Untar then call base installer."""
        PackageUtil.UnTarFile( self._TarName, self.GetInstallPath(), 1 )
        super( AvalancheRelease, self )._Install()
