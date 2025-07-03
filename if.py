# When a user interacts with an ATM, the software in the ATM can use branching to 
# decisions based on the user's input. For example, if the user selects "Withdraw Cash"
# the ATM can branch into different denominations of bills to dispense based on the amount requested.

User_choice="Withdraw Cash"
if User_choice=="Withdraw Cash":
    amount=int(input("amount:"))
    if amount%10==0:
        print(" dispensed amount",amount)
    else:
        print("please enter a multiple of 10")
else:
    print("Thanks for using ATM")
print("Thanks for using ATM")


def city_checker():
    '''if chapter exercise (a)'''

    usa = ["atlanta", "new york", "chicago", "baltimore"]
    uk = ["london", "bristol", "cambridge"]
    india = ["mumbai", "delhi", "banglore"]

    city = input("Enter city name: ")

    if city in usa:
        print(city,"is in usa")
    elif city in uk:
        print(city,"is in uk")
    elif city in india:
        print(city,"is in india")
    else:
        print("I won't be able to tell you which country",city,"is in! Sorry!")



    
    


