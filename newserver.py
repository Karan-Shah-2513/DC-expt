from operator import truediv
# import xmlrpc.client
from time import sleep
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
# Restrict to a particular path.
import json

# f = open('db.json')

# data = json.load(f)


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


priority = input("Enter priority: ")
# Create server
PORT_NUMBER = 8000
if priority == '1':
    PORT_NUMBER = 8000
if priority == '2':
    PORT_NUMBER = 8001
if priority == '3':
    PORT_NUMBER = 8002
with SimpleXMLRPCServer(('localhost', PORT_NUMBER),
                        requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()

    # Register pow() function; this will use the value of
    # # pow.__name__ as the name, which is just 'pow'.
    # server.register_function(pow)

    # Register a function under a different name
    # def adder_function(x, y):
    #     return x + y
    # server.register_function(adder_function, 'add')

    # Register an instance; all the methods of the instance are
    # published as XML-RPC methods (in this case, just 'mul').
    class MyFuncs:
        # def mul(self, x, y):
        #     return x * y
        def amIworking(self):
            return True

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
