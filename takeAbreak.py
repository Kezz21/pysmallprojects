import time
import webbrowser



loopcount = 0

print("This program started on ", (time.ctime()))
while loopcount < 3:

    # Take a break every 30 sec
    time.sleep(30)
    webbrowser.open("https://www.youtube.com/watch?v=rW7e7XpQ24I")

    loopcount +=1

