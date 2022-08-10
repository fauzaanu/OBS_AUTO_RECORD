# OBS AUTO RECORD
Script to start OBS Recording when a certain program is running. And to exit when that program exits. Hardcoded for illustrator.

Script is meant to be running continuously from system startup
## Libraries Used
- psutil~=5.9.1
- ~~pywinauto~~
- ~~pyautogui~~


## USAGE & INSTALLATION
`pip install -r requirements.txt`

In an empty python File:

```
from obs_auto_rec import Recorder

if __name__ == "__main__":
    while 1 == 1:
        # monitor Application
        Recorder(monitor_application="illustrator", scene="FS", recheck_delay=3)
```


`monitor_application="illustrator"` : Should be the name you see on Windows task
manager. It is not necessary to keep full name.

`scene="FS"` : This is the obs scene you want to record. FS is just a scene name 
i have to refer to record full screen. As scene switching have not been made possible yet,
it is best to record the full screen. In Future, Scene should be switched automatically
based on the program window the user is intaracting with.

`recheck_delay=3` : When both obs and illustrator is reporting inactivity is not useful
to keep rechecking for the same application. This delay in seconds will break the loop
inside of the Class Recorder. This is also why the sameple code includes a loop so the 
checking will go on forever. But it is more useful when it breaks as now we can add another
program to check for.


## Important
- Record in mkv (still might corrupt) : From around 20 test recordings that were recorded in mkv only 3 got corrupt.
- To fully automate in the background:
  - use a bat file 
  - run it via pythonw.exe rather than python.exe
  - shebang line must be present on top of python file (my_script.pyw)
  - Example: `#! C:\Users\{user}\Desktop\OBS_AUTO_RECORD\venv\Scripts\pythonw.exe`
  - save python file with .pyw

## TODO
- ~~[ ]  Add pyautogui and send the hotkey~~ : HOTKEYS NOT WORKING
- ~~[ ] Add pyauto gui and detect the start recording and stop recording button~~
- [x] Change structure to add more programs instead of 1
- [ ] Scene Switcher: Scene Switching based on what the user is interacting with
