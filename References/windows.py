# for making a windows exe file: not ideal for my case as customization is not possible easily
# eg: pyinstaller --onefile windows.py

from obs_auto_rec import Recorder

if __name__ == "__main__":
    try:
        names = input("Type all program names to monitor in this syntax: (prog1,prog2,)\n")
        progs = names.split(",")

        delay = input("Checking delay? (seconds)\n")


        while 1 == 1:
            for prog in progs:
                Recorder(monitor_application=f"{prog}", scene="AI", recheck_delay=int(delay))
    except Exception(BaseException) as f:
        # print('error: ' + str(f))
        pass


