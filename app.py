import threading
import os
import time


def print_cube(num):
    time.sleep(10)
    for i in range(100):
        os.system("echo hey")


def print_square(num):
    for i in range(100):
        os.system("echo hey1")


if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_cube, args=(10,))

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
