from operator import truediv
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import pandas as pd
# Restrict to a particular path.
import json

f = open('db.json')

data = json.load(f)


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Create server
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
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

        def calculateMyBill(self, unit):
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
            return total
            # print("Electricity bill is %.2f" % total)

        def findId(self, id):
            for i in data["dataset"]:
                # print(i)
                print(i['ID'])
                if int(i['ID']) == int(id):
                    return int(i['Units'])
            return 0

    server.register_instance(MyFuncs())

    # Run the server's main loop
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, Exiting\n")
        exit(0)
