import os

# A script to locate a file

def locate(file):
   for root, dirs, files in os.walk('C:\\'):
       if file in files:
           print(root, file)
   print('Finish')
   input()

try:
   s=input('name: ')
   locate(s)
except:
   None