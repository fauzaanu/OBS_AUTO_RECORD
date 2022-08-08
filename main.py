from psutil import process_iter
from subprocess import Popen


def isitrunning(names):
    processlist = []
    status = {}

    for process in process_iter():
        processlist.append(process.name().casefold())

    # print(processlist)
    for name in names:
        status[name] = "inactive"
        # print(name.casefold())

        for procesx in processlist:
            if str(name.casefold()) in procesx:
                status[name] = "active"

    return status


def recheck(old_status):
    current_status = isitrunning(["illustrator", "obs64"])

    if old_status != current_status:
        old_status = current_status
        print(current_status)

    if current_status["illustrator"] == "active" and current_status["obs64"] == "inactive":
        print("Opening OBS")
        x = Popen(['C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe', '--startrecording', '--minimize-to-tray'],
                  cwd="C:\\Program Files\\obs-studio\\bin\\64bit\\", )

    if current_status["illustrator"] == "inactive" and current_status["obs64"] == "active":
        for process in process_iter():
            if "obs64" in str(process.name()).casefold():
                print("Killing OBS")
                process.kill()

    return old_status


if __name__ == "__main__":

    # When illustrator is running but OBS is not start OBS and start recording
    # OBS should be recording mkv so when we force close it the files still will be saved
    current_status = dict()
    old_status = dict()
    current_status = isitrunning(["illustrator", "obs64"])
    if old_status != current_status:
        print(current_status)
        old_status = current_status

    if current_status["illustrator"] == "active" and current_status["obs64"] == "inactive":
        print("Opening OBS")
        x = Popen(['C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe', '--startrecording', '--minimize-to-tray'],
                  cwd="C:\\Program Files\\obs-studio\\bin\\64bit\\", )
        recheck(old_status)

    if current_status["illustrator"] == "inactive" and current_status["obs64"] == "active":
        for process in process_iter():
            if "obs64" in str(process.name()).casefold():
                print("Killing OBS")
                process.kill()
        recheck(old_status)

    while current_status["illustrator"] == "inactive" and current_status["obs64"] == "inactive" \
            or current_status["illustrator"] == "active" and current_status["obs64"] == "active":
        old_status = recheck(old_status)
