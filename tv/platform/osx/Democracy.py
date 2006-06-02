import os
import sys
import Foundation

# =============================================================================

def launchDemocracy():
    # We can now import our stuff
    import app
    import prefs
    import config

    # Tee output off to a log file
    class AutoflushingTeeStream:
        def __init__(self, streams):
            self.streams = streams
        def write(self, *args):
            for s in self.streams:
                s.write(*args)
                s.flush()

    logFile = config.get(prefs.LOG_PATHNAME)
    if logFile:
        h = open(logFile, "wt")
        sys.stdout = AutoflushingTeeStream([h, sys.stdout])
        sys.stderr = AutoflushingTeeStream([h, sys.stderr])

    # Kick off the application
    app.main()

# =============================================================================

def launchDownloaderDaemon():
    import imp
    mfile, daemonPath, mdesc = imp.find_module('dl_daemon')
    daemonPrivatePath = os.path.join(daemonPath, 'private')
    sys.path[0:0] = [daemonPath, daemonPrivatePath]
    import Democracy_Downloader

# =============================================================================

# If the bundle is an alias bundle, we need to tweak the search path
bundle = Foundation.NSBundle.mainBundle()
bundleInfo = bundle.infoDictionary()
if bundleInfo['PyOptions']['alias']:
    root = os.path.dirname(bundle.bundlePath())
    root = os.path.join(root, '..', '..')
    root = os.path.normpath(root)
    sys.path[0:0] = ['%s/portable' % root]

if len(sys.argv) > 1 and sys.argv[1] == "download_daemon":
    launchDownloaderDaemon()
else:
    launchDemocracy()

