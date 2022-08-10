# OBS AUTO RECORD
Script to start OBS Recording when a certain program is running. And to exit when that program exits. Hardcoded for illustrator.

Script is meant to be running continousely from system startup

## Important
- Record in mkv (still might corrupt) : From around 20 test recordings that were recorded in mkv only 3 got corrupt.
- To fully automate in the background:
  - use a bat file 
  - run it via pythonw.exe rather than python.exe
  - shebang line must be present on top of python file (AIPS.pyw)
  - save python file with .pyw

## TODO
- [ ]  ~~Add pyautogui and send the hotkey~~ : HOTKEYS NOT WORKING
- [ ] Add pyauto gui and detect the start recording and stop recording button
- [x] Change structure to add more programs instead of 1
