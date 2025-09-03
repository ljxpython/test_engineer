from functools import reduce



from threading import Thread
from multiprocessing import Process

from threading import Lock

from queue import Queue

def thread_1():
    print(f"thread_i")


def thread_2():
    print(f"thread_2")

t1 = Thread(target=thread_1)
t2 = Thread(target=thread_2)

t1.start()
t2.start()

t1.join()
t2.join()



