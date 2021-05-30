from multiprocessing import Process, Queue

def tripler(mylist, q):
    """
    function to triple items in a given list
    """
    # append triples of mylist to queue
    for num in mylist:
       q.put(num * 3)

def print_queue(q):
    """
    function to print queue elements
    """
    print("Queue elements:")
    while not q.empty():
        print(q.get())
    print("Queue is now empty!")

if __name__ == "__main__":
    # input list
    mylist = [1,2,3,4]

    # creating multiprocessing Queue
    q = Queue()

    # creating new processes
    p1 = Process(target=tripler, args=(mylist, q))
    p2 = Process(target=print_queue, args=(q,))

    # running process p1 to square list
    p1.start()
    p1.join()

    # running process p2 to get queue elements
    p2.start()
    p2.join()

