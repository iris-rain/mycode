from multiprocessing import Process, Pipe
import time

def print_result(conn):
    print(conn.recv())
    conn.send("received the result")
    conn.close()

def tripler(mylist, conn):
    for ind, item in enumerate(mylist):
        mylist[ind] = item * 3
    # sends or returns data through the pipe -as child_conn
    time.sleep(5)
    conn.send(mylist)
    print(conn.recv())
    # closes connection to pipe - so others may use it next
    conn.close()

if __name__ == '__main__':
    # sets pipe ends
    parent_conn, child_conn = Pipe()
    nums = [3, 4, 5, 6]
    p = Process(target=tripler, args=(nums, child_conn,))
    p.start()
    # print what parent process received
    p2 = Process(target=print_result, args=(parent_conn,))
    p2.start()
    #print(child_conn.recv())   
    p.join()

