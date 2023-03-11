# import time
# def countdown(n):
#     while n > 0:
#         print('T-minus',n)
#         n -= 1
#         time.sleep(1)

# from threading import Thread
# t = Thread(target=countdown,args=(10,),daemon=True)
# t.start()
# time.sleep(10)
# if t.is_alive():
#     print('Still running')
# else:
#     print('Completed')


from threading import Thread, Event
import time

# Code to execute in an independent thread
def countdown(n, started_evt):
    print('countdown starting')
    started_evt.set()
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)

# Create the event object that will be used to signal startup
started_evt = Event()

# Launch the thread and pass the startup event
print('Launching countdown')
t = Thread(target=countdown, args=(10,started_evt))
t.start()

# Wait for the thread to start
started_evt.wait()
print('countdown is running')