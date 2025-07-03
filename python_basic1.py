
# After flipping a coin 10 times you got this result,
result = ["heads","tails","tails","heads","tails","heads","heads","tails","tails","tails"]
# Using for loop figure out how many times you got heads
count=0
for i in result:
    if i=="heads":
        count+=1
    
print("count of heads is", count)
# Print square of all numbers between 1 to 10 except even numbers
for i in range(1,11):
    if i%2!=0:
        continue
    print(i**2)
# Your monthly expense list (from Jan to May) looks like this,
expense_list = [2340, 2500, 2100, 3100, 2980]
for i in range(len(expense_list)):
    expense=expense_list[i]
    print(f"in month {i+1} you spent {expense} dollars")
    
# Lets say you are running a 5 km race. Write a program that,

# Upon completing each 1 km asks you "are you tired?"
# If you reply "yes" then it should break and print "you didn't finish the race"
# If you reply "no" then it should continue and ask "are you tired" on every km
# If you finish all 5 km then it should print congratulations message
for km in range(1,6):
    print(f"you have completed {km} km.")
    tired=input("are you tired?:")
    
    if tired=="yes":
        break
if km==5:
    print("congratulations! you finished")
else:
    print("you didn't finish")
# 5. Write a program that prints following shape
# ```
# *
# **
# ***
# ****
# *****
for i in range(1,6):
    s=""
    for j in range(i):
        s+="*"
    print(s)
    
print("Functon")
# Write a function called calculate_area that takes base and height as an input
# and returns and area of a triangle. Equation of an area of a triangle is,
def calculate_area(base,height):
    area=.5*base*height
    return area 
b=int(input("value of base:"))
h=int(input("value of height:"))
result=calculate_area(b,h)
print(result)



