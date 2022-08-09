from psutil import process_iter
from subprocess import Popen
import time


# OOP - Testing
class Recorder:
    def __init__(self, monitor_application, scene, recheck_delay):
        self.monitor_application = monitor_application
        self.scene = scene
        self.start_time = time.time()
        self.inactivity_delay = recheck_delay

        self.break_next = False

        current_status = dict()

        # Should not always run, After killing OBS Give back control.
        # Deciding to keep checking should be a per instance decision rather than fixed in the class
        # now we have recheck_delay to end the rechecking on inactivity
        while not self.break_next:
            current_status = self.recheck(current_status)

    def isitrunning(self, names):
        processlist = []
        status = {}


        for process in process_iter():
            processlist.append(process.name().casefold())

        for name in names:
            status[name] = "inactive"

            for procesx in processlist:
                if str(name.casefold()) in procesx:
                    status[name] = "active"

        return status

    def obs_kill_safe(self, process):

        # hot keys are not working -- Need to find a more reliable way
        print("Killing OBS")
        process.kill()
        self.break_next = True

    def status_reporter(self, old_status):
        current_status = self.isitrunning([f"{self.monitor_application}", "obs64", ])
        if old_status != current_status:
            print(current_status)

        return current_status

    def open_obs(self, scene_name):
        print("Opening OBS")
        x = Popen(['C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe', '--startrecording', '--minimize-to-tray',
                   f'--scene {scene_name}'],
                  cwd="C:\\Program Files\\obs-studio\\bin\\64bit\\", )

    def recheck(self, old_status):
        current_status = self.status_reporter(old_status)

        if current_status[f"{self.monitor_application}"] == "inactive" and current_status[
            "obs64"] == "inactive":
            started_on = self.start_time
            duration = time.time() - started_on

            if duration > self.inactivity_delay:
                self.break_next = True

        if current_status[f"{self.monitor_application}"] == "active" and current_status[
            "obs64"] == "inactive":
            self.open_obs("FS")

        if current_status[f"{self.monitor_application}"] == "inactive" and current_status[
            "obs64"] == "active":
            for process in process_iter():
                if "obs64" in str(process.name()).casefold():
                    self.obs_kill_safe(process)
        return current_status


