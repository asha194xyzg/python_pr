# variable
birth_year=2002
Current_year=2025
print("Age:",Current_year-birth_year)
first_name="ASHA"
Last_name="ALIN"
print("full name:",first_name,Last_name)
# area of triangle
base= 19.68
hight=24.70
area=.5*base*hight
print("Area of triangle:",area)
# area of rectangle
length= 10.5
width= 7.6
area_of_rectangle=length*width
print("Area of rectangle:",area_of_rectangle)
# area of circle
import math
radius= 5.5
area_of_circle=math.pi*radius**2
print("Area of circle:",area_of_circle)
# area of square
side= 4.5
area_of_square=side**2
print("Area of square:",area_of_square)
# complex number
a=3+7j
b=6-2j
c=a-b
print("complex number:",c)
# address
street="house no 12,road no 5"
city="Dhaka"
country="Bangladesh"
address=street+" "+city+" ,"+country
print("Address:",address)
print(f"Address:{street},{city},{country}")
# 2. Create a variable to store the string "Earth revolves around the sun"
#     1. Print "revolves" using slice operator
#     2. Print "sun" using negative index
earth_string = "Earth revolves around the sun"
print("Slice operator - 'revolves':", earth_string[6:14])
print("Negative index - 'sun':", earth_string[-3:])

# 3. Create two variables to store how many fruits and vegetables you eat in a day.
# Now Print "I eat x veggies and y fruits daily" where x and y presents vegetables and fruits that you eat everyday.
# Use python f string for this.
fruits=10
vegetables=7
print(f"I eat {vegetables} veggies and {fruits} fruits daily")
# 4. I have a string variable called s='I eat 200 banana'. This of course is a
# wrong statement, the correct statement is 'I eat 10 samosa '.
# Replace incorrect words in original strong with new ones and print the new string.
# Also try to do this in one line.
s="I eat 200 banana"
s=s.replace("200 banana","10 samosa")
print("Corrected string:", s)
# append,extend,insert
foods=["samosa","burger","pizza"]
foods.append("pasta")
foods.extend(["salad","fries"])
foods.insert(1,"sandwich")
print("Updated food list:", foods)
# dfference between append, extend 
f=["apple","banana","cherry"]
f.append(["orange", "grape"])  # Appends a list as a single element
print("After append:", f)
del f[-1]
print("After delete last element:", f)
f.extend(["kiwi", "mango"])  # Extends the list by adding elements
print("After extend:", f)
print(f[1:4])
# 2. Write a program that takes file name with extension as an input and
# prints just the file name without extension (you can assume that file extensions
# are always 3 character long)
# file_name=input("enter the file_name with extension: ")
# file_name_without_extension = file_name[:-4]# Assuming extension is always 3 characters long + 1 dot
# print("File name without extension:", file_name_without_extension)
# 1. Let us say your expense for every month are listed below,
# 	1. January -  2200
#  	2. February - 2350
#     3. March - 2600
#     4. April - 2130
#     5. May - 2190
L=[2200,2350,2600,2130,2190]

# Create a list to store these monthly expenses and using that find out,
print(L)
# 1. In Feb, how many dollars you spent extra compare to January?
# 2. Find out your total expense in first quarter (first three months) of the year.
# 3. Find out if you spent exactly 2000 dollars in any month
# 4. June month just finished and your expense is 1980 dollar. Add this item to our monthly expense list
# 5. You returned an item that you bought in a month of April and
# got a refund of 200$. Make a correction to your monthly expense list
# based on this
L1=L[1]-L[0]
print("compare dollars from feb to january:",L1)
print("total expense in first three month:",L[0]+L[1]+L[2])
if L==2000:
    print("true")
else:
    print("Flase")
# or
print(2000 in L)    
L.append(1980)
print(L)
L2=L[3]-20
print(L2)
heros=['spider man','thor','hulk','iron man','captain america']
print("lenth of the list:",len(heros))
# 2. Add 'black panther' at the end of this list
heros.append("black panther")
print(heros)
# 3. You realize that you need to add 'black panther' after 'hulk',
# so remove it from the list first and then add it after 'hulk'
heros.remove("black panther")
heros.insert(2,"black panther")
print(heros)
heros.remove("black panther")
heros.insert(3,"black panther")
print(heros)
# if ,elif,else
fruit1=["apple","banana","orange","mango"]
fruit2=["kiwi","grape","watermelon"]
fruit3=["pineapple","strawberry","blueberry"]
fruit=input("Enter your favorite fruit: ")
if fruit in fruit1:
    print(f"{fruit} is in the first list of fruits.")
elif fruit in fruit2:
    print(f"{fruit} is in the second list of fruits.")
else:
    print(f"{fruit} is in the third list of fruits.")
    
india = ["mumbai", "banglore", "chennai", "delhi"]
pakistan = ["lahore","karachi","islamabad"]
bangladesh = ["dhaka", "khulna", "rangpur"]
city=input("Enter a city name: ")
if city in india:
    print(f"{city} is in India")
elif city in pakistan:
    print(f"{city} is in Pakistan")
elif city in bangladesh:
    print(f"{city} is in Bangladesh")
#     Write a program that asks user to enter a city name and it should tell which country the city belongs to
# Write a program that asks user to enter two cities and it tells you if they both are in same country or not. For example if I enter mumbai and chennai, it will print "Both cities are in India" but if I enter mumbai and dhaka it should print "They don't belong to same country"
# Write a python program that can tell you if your sugar is normal or not. Normal fasting level sugar range is 80 to 100.
# Ask user to enter his fasting sugar level
# If it is below 80 to 100 range then print that sugar is low
# If it is above 100 then print that it is high otherwise print that it is normal
citi1=input("Enter first city name: ")
city2=input("Enter second city name: ")
if citi1 in india and city2 in india:
    print("Both cities are in India")
elif citi1 in pakistan and city2 in pakistan:
    print("Both cities are in Pakistan")
elif citi1 in bangladesh and city2 in bangladesh:
    print("Both cities are in Bangladesh")
else:
    print("They don't belong to same country")
    
# 2. Write a python program that can tell you if your sugar is normal or not.
# Normal fasting level sugar range is 80 to 100.
suger=int(input("Enter your fasting sugar level: "))
if suger>=80 and suger<100:
    print("Your sugar level is normal.")
else:
    print("Your sugar level is not normal.")
    
# 2
suger1=int(input("Enter your fasting sugar level: "))

if suger1>80 and suger1<=100:
    print("Your sugar level is normal.")
elif suger1>100:
    print("Your sugar level is high.")
else:
    print("Your sugar level is low.")
