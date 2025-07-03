# You are given following list of stocks and their prices in last 3 days,

# Stock	Prices
# info	[600,630,620]
# ril	[1430,1490,1567]
# mtl	[234,180,160]
# Write a program that asks user for operation. Value of operations could be,
# print: When user enters print it should print following,
# info ==> [600, 630, 620] ==> avg:  616.67
# ril ==> [1430, 1490, 1567] ==> avg:  1495.67
# mtl ==> [234, 180, 160] ==> avg:  191.33
# add: When user enters 'add', it asks for stock ticker and price. If stock already
#exist in your list (like info, ril etc) then it will append the price to the list. 
# Otherwise it will create new entry in your dictionary. For example entering 'tata' 
# and 560 will add tata ==> [560] to the dictionary of stocks.



import statistics

stocks = {
    'info': [600,630,620],
    'ril': [1430,1490,1567],
    'mtl': [234,180,160]
}

def print_all():
    for stock,price in stocks.items():
        avg=statistics.mean(price)
        print(f"{stock}==>{price}==>avg:{round(avg,3)}")
def add():
    s=input("enter a stock name:")
    p=input("enter the price:")
    p=int(p)
    if s in stocks:
        stocks[s].append(p)
    else:
        stocks[s]=[p]
    print_all()
def main():
    op=input("enter operator(add,print):").lower()
    if op=="add":
        add()
    elif op=="print":
        print_all()
    else:
        print("unsuport operation",op)

if __name__ == '__main__':
    main()
    
    
# Write circle_calc() function that takes radius of a circle as an input from user and 
# then it calculates and returns area, circumference and diameter. 
# You should get these values in your main program by calling circle_calc function and then print them
import math
def circle_calc(radius):
    area=math.pi*radius*radius
    circumference=2*math.pi*radius
    diameter=2*radius
    return area,circumference,diameter
# r=int(input("radius:"))
# result=circle_calc(r)
# print(result)
if __name__=="__main__":
    r=int(input("radius:"))
    area,circumference,diameter=circle_calc(r)
    print(f"area:{area}, circumference:{circumference},diameter:{diameter}")