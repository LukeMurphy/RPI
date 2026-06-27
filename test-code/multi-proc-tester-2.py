from multiprocessing import Process, Pipe

def worker(conn):
    conn.send("Message from worker")
    msg = conn.recv()
    print("Worker got:", msg)
    conn.close()

def worker2(conn):
    conn.send("Message from worker2")
    msg = conn.recv()
    print("Worker2 got:", msg)
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()

    p = Process(target=worker, args=(child_conn,))
    p.start()

    p2 = Process(target=worker2, args=(parent_conn,))
    p2.start()

    print("\n--------")
    print("\nParent got:", parent_conn.recv())
    parent_conn.send("Ack from parent")
    p.join()
    print("\nChild got:", child_conn.recv())
    child_conn.send("foo from child")

    p2.join()