import time
t=time.strftime("%H:%M:%S")
Hour=int(time.strftime("%H"))
print(Hour)
if Hour>=0 and Hour<12: 
    print("Good morning sir")
elif Hour>=12 and Hour<18:
    print("Good afternOOn sir")
elif Hour>=18 and Hour<24:
    print("Good night")

    