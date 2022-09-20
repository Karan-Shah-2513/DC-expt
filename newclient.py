import xmlrpc.client
import pandas as pd
from datetime import datetime
s = xmlrpc.client.ServerProxy('http://localhost:8000')
# print(s.pow(2, 3))  # Returns 2**3 = 8
# print(s.add(2, 3))  # Returns 5
# print(s.mul(5, 2))  # Returns 5*2 = 10

# # Print list of available methods
# print(s.system.listMethods())

# print("\nThe Electricity Bill is : ", s.calculateBill(3, 5))

id = input('Enter your id : ')
#

units, due_date, name = s.findId(id)
if units and due_date:
    print("User Name: "+name)
    print("Due Date: "+due_date)
    print("Units Consumed: "+str(units))
    print("Final Bill Amount: ")

    print(s.calculateMyBill(units, due_date))

    pay_bill = input('Press 1 to pay bill or 2 to exit: ')
    if pay_bill == '1':
        today_date = datetime.now()
        print("Successfull payment on "+str(datetime.now())+"\nThank you!")
    else:
        print("Thankyou visit again")
else:
    print('Id not found')
