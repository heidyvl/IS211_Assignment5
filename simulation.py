import random
import csv
from StringIO import StringIO
import urllib2
import time
import argparse


class Queue:
    def __init__(self):
        self.items = []
    def is_empty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0,item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)

class Server:
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0
    def tick(self):
        if self.current_task != None:
            self.time_remaining = int(self.time_remaining) - 1
        if self.time_remaining <= 0:
            self.current_task = None
    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False
    def start_next(self,new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_time()
        
class Request:
    def __init__(self, time, process_time):
        self.timestamp = time
        self.process_time = process_time
    def get_stamp(self):
        return self.timestamp
    def get_time(self):
        return self.process_time
    def wait_time(self, current_time):
        return current_time - self.timestamp

def simulateOneServer(filename):
    server_queue = Queue()
    waiting_times = []
    server = Server ()
    for row in filename:
        second_request = int(row[0])
        process_time = row[2]
        request = Request(second_request, process_time)
        server_queue.enqueue(request)
        if (not server.busy()) and (not server_queue.is_empty()):
            next_request = server_queue.dequeue()
            waiting_times.append(next_request.wait_time(int(second_request)))
            server.start_next(next_request)
        server.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    return average_wait

def simulateManyServers(filename, servers):
    server_queue = Queue()
    waiting_times = []
    server = Server ()
    serverlist = []
    for number in range(servers):
        serverlist.append(Server())
    for server in serverlist:
        for row in filename:
            second_request = int(row[0])
            process_time = row[2]
            request = Request(second_request, process_time)
            server_queue.enqueue(request)
            if (not server.busy()) and (not server_queue.is_empty()):
                next_request = server_queue.dequeue()
                waiting_times.append(next_request.wait_time(int(second_request)))
                server.start_next(next_request)
            server.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    return average_wait
    
def read_url(weburl):
    response = urllib2.urlopen(weburl)
    return response.read()
    
def parse_data(csvdata):
    newlist = []
    reader = csv.reader(StringIO(csvdata))
    for row in reader:
        newlist.append(row)
    return newlist

  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='enter number of servers.')
    parser.add_argument('-s', '--servers', action="store", dest="servers")
    args = parser.parse_args()
    if not args.servers:
        print "Average Wait Time is for one server is %6.2f secs." % simulateOneServer(parse_data(read_url("http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv")))
    else:
        print "Average Wait Time is for multiservers is %6.2f secs." % simulateManyServers(parse_data(read_url("http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv")), int(args.servers))
    
