# This is for testing scene switcher module

from win32gui import GetWindowText, GetForegroundWindow
from obswebsocket import obsws, requests  # noqa: E402

from psutil import process_iter
from subprocess import Popen
import time


# OOP - Testing
class Recorder:
    def __init__(self, monitor_application, scene_data, recheck_delay):
        self.monitor_application = monitor_application
        self.scene_data = scene_data
        self.start_time = time.time()
        self.inactivity_delay = recheck_delay

        self.break_next = False
        self.we_opened_obs = False
        self.code = 0

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
        self.we_opened_obs = True
        x = Popen(['C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe', '--startrecording', '--minimize-to-tray',
                   f'--scene {scene_name}'],
                  cwd="C:\\Program Files\\obs-studio\\bin\\64bit\\", )

    def recheck(self, old_status):
        current_status = self.status_reporter(old_status)

        while current_status["obs64"] == "active":
            for scene, applications in self.scene_data.items():
                for app in applications:
                    is_active = self.get_active(app)
                    if is_active:
                        self.scene_switcher(scene)

        if current_status[f"{self.monitor_application}"] == "inactive" and current_status[
            "obs64"] == "inactive":
            started_on = self.start_time
            duration = time.time() - started_on
            self.code = 102

            if duration > self.inactivity_delay:
                self.break_next = True

        if current_status[f"{self.monitor_application}"] == "active" and current_status[
            "obs64"] == "inactive":
            self.open_obs("FS")
            self.code = 101

        if current_status[f"{self.monitor_application}"] == "inactive" and current_status[
            "obs64"] == "active":
            self.code = 100
            for process in process_iter():
                if "obs64" in str(process.name()).casefold():
                    if self.we_opened_obs:
                        self.obs_kill_safe(process)
        return current_status

    def scene_switcher(self, scene):
        host = "localhost"
        port = 4444
        password = "1234"

        ws = obsws(host, port, password)
        ws.connect()

        try:
            scenes = ws.call(requests.GetSceneList())
            for s in scenes.getScenes():
                if scene == s['name']:
                    name = s['name']
                    print(u"Switching to {}".format(name))
                    ws.call(requests.SetCurrentScene(name))
                    time.sleep(2)
            print("End of list")

        except KeyboardInterrupt:
            pass

        ws.disconnect()

    def get_active(self, application):
        window_name = GetWindowText(GetForegroundWindow())
        if str(application).casefold() in str(window_name).casefold():
            return True
        else:
            return False


if __name__ == "__main__":
    scene_data = {
        "AI": ['Illustrator'],
        "CAL": ['Calculat'],
        "PS": ['Photoshop']
    }

    Illustrator = Recorder(monitor_application="illustrator", scene_data=scene_data, recheck_delay=3)
    Photoshop = Recorder(monitor_application="illustrator", scene_data=scene_data, recheck_delay=3)
