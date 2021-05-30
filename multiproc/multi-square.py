from multiprocessing import Process, current_process
import os

def squarer(number):
    """
    A squaring function that can be used by a process
    """
    result = number ** 2
    proc_name = current_process().name
    print('{0} squared to {1} by: {2}-{3}'.format(
        number, result, proc_name, os.getpid()))

if __name__ == '__main__':
    numbers = [2, 3, 4, 5, 6]
    procs = []
    for number in numbers:
        proc = Process(target=squarer, args=(number,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()


