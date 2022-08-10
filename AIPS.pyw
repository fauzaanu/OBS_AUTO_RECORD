#! C:\Users\Fauzaanu\Desktop\OBS_AUTO_RECORD\venv\Scripts\pythonw.exe
from obs_auto_rec import Recorder

if __name__ == "__main__":
    while 1 == 1:
        # monitor illustrator
        Recorder(monitor_application="illustrator", scene="AI", recheck_delay=3)

        # monitor photoshop
        Recorder(monitor_application="photoshop", scene="PS", recheck_delay=3),

        # add more as you wish

        # monitor_application: partial text will be fine: Repeating texts might be bad
        # scene: OBS SCENE NAME
        # recheck_delay: When should the rechecking stop so YOU can monitor the second program
        # Above case: monitored for AI for 3 secs and if inactivity is seen the monitoring is stopped
        # so now the monitoring starts for photoshop and if inactive the loop starts again

# Top line needed if trying to run in windows in the background: to run it should call pyw instead of py on win 11
# (pythonw.exe)
