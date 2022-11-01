from operator import truediv
from time import sleep
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
# Restrict to a particular path.
import json


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# priority = input("Enter priority: ")
# Create server
PORT_NUMBER = 8003


PORT1 = 8000
PORT2 = 8001
PORT3 = 8002
server1 = xmlrpc.client.ServerProxy(f'http://localhost:{PORT1}')
server2 = xmlrpc.client.ServerProxy(f'http://localhost:{PORT2}')
server3 = xmlrpc.client.ServerProxy(f'http://localhost:{PORT3}')


def isServerWorking(temp):
    try:
        return temp.amIworking()
    except:
        return False


# Register pow() function; this will use the value of
# # pow.__name__ as the name, which is just 'pow'.
# server.register_function(pow)

# Register a function under a different name
# def adder_function(x, y):
#     return x + y
# server.register_function(adder_function, 'add')

# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'mul').
with SimpleXMLRPCServer(('localhost', PORT_NUMBER),
                        requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()

    class MyFuncs:
        # def mul(self, x, y):
        #     return x * y
        def sendPORT(self):
            PORT = PORT_NUMBER
            if(isServerWorking(server1)):
                PORT = PORT1
            elif(isServerWorking(server2)):
                PORT = PORT2
            elif(isServerWorking(server3)):
                PORT = PORT3

            print(PORT, " is working")
            return PORT

        def calculateMyBill(self, unit, due_date):
            if (unit <= 600):
                pay = unit*3
                charge = 50
            elif (unit <= 700):
                pay = (600*3.00) + (unit - 600)*3.75
                charge = 60.00
            elif (unit <= 800):
                pay = (600*3.00) + (100*3.75) + (unit - 700)*4.00
                charge = 65.00
            elif (unit <= 900):
                pay = (600*3.00) + (100*3.75) + (100*4) + (unit - 800)*4.50
                charge = 70.00
            elif (unit <= 1000):
                pay = (600*3.00) + (100*3.75) + (100*4) + \
                    (100*4.50) + (unit - 900)*5.00
                charge = 75.00
            total = pay + charge
            fine = 0
            today_date = datetime.now()
            due_date_format = datetime.strptime(due_date, '%d/%m/%y %H:%M:%S')
            if due_date_format < today_date:
                fine = 0.2*total
            return (total+fine)
            # print("Electricity bill is %.2f" % total)

        def findId(self, id):
            f = open('db.json')
            data = json.load(f)
            for i in data["dataset"]:
                # print(i)
                # print(i['ID'])
                if int(i['ID']) == int(id):
                    print("Due date: "+i['Due_Date'])
                    return int(i['Units']), i['Due_Date'], i['Name']
            return 0

        def updateDueDate(self, id):
            f = open('db.json')
            data = json.load(f)
            while data["lock"]:
                print('Waiting for db')
                sleep(3.0)
            f.close()
            f = open('db.json', "r+")
            data = json.load(f)
            data["lock"] = 1
            for i in data["dataset"]:
                # print(i)
                # print(i['ID'])
                if int(i['ID']) == int(id):
                    i['Due Date'] = str(
                        datetime.today() + relativedelta(months=+1))
                    print('New Due Date:', i['Due Date'])
                    break
            sleep(3.0)
            data["lock"] = 0
            f.close()

    server.register_instance(MyFuncs())

    # Run the server's main loop
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, Exiting\n")
        exit(0)
