import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import win32evtlogutil
import os
import sys
import string
import time
import servicemanager

class Service(win32serviceutil.ServiceFramework):
   
    _svc_name_ = "RT24 Performance Test"
    _svc_display_name_ = "RT24 Performance Test"
    _svc_description_ = "RT24 Performance Test"
         
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)           

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)                    
        
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, '')) 
      
        # This is how long the service will wait to run / refresh itself (see script below)
        self.timeout = 10000

        while 1:
            # Wait for service stop signal, if I timeout, loop again
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            # Check to see if self.hWaitStop happened
            if rc == win32event.WAIT_OBJECT_0:
                # Stop signal encountered
                servicemanager.LogInfoMsg("The RT24 Performance Test service has stopped.")  #For Event Log
                break
            else:
                try:
                    os.system("python d:\\user\\ygu5\\project\\rt24\\check-update.py")
                    os.system("python d:\\user\\ygu5\\project\\rt24\\run-test.py")
                except:
                    pass 


def ctrlHandler(ctrlType):
    return True
                  
if __name__ == '__main__':   
    win32api.SetConsoleCtrlHandler(ctrlHandler, True)   
    win32serviceutil.HandleCommandLine(Service)