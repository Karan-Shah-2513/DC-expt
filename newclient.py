import xmlrpc.client
import pandas as pd

s = xmlrpc.client.ServerProxy('http://localhost:8000')
# print(s.pow(2, 3))  # Returns 2**3 = 8
# print(s.add(2, 3))  # Returns 5
# print(s.mul(5, 2))  # Returns 5*2 = 10

# # Print list of available methods
# print(s.system.listMethods())

# print("\nThe Electricity Bill is : ", s.calculateBill(3, 5))

id = input('Enter your id : ')
#

units = s.findId(id)
if units:
    print(s.calculateMyBill(units))
else:
    print('Id not found')
