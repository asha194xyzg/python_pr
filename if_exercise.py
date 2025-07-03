## Exercise: Python If Condition
# 1. Using following list of cities per country,
#     ```
#     india = ["mumbai", "banglore", "chennai", "delhi"]
#     pakistan = ["lahore","karachi","islamabad"]
#     bangladesh = ["dhaka", "khulna", "rangpur"]
#     ```
# Write a program that asks user to enter a city name and it should tell which country the city belongs to
    
india = ["mumbai", "banglore", "chennai", "delhi"]
pakistan = ["lahore","karachi","islamabad"]
bangladesh = ["dhaka", "khulna", "rangpur"]
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
# 1. Using following list of cities per country,
#     ```
#     india = ["mumbai", "banglore", "chennai", "delhi"]
#     pakistan = ["lahore","karachi","islamabad"]
#     bangladesh = ["dhaka", "khulna", "rangpur"]
#     ```
#Write a program that asks user to enter two cities and it tells you if they both
# are in same country or not. For example if I enter mumbai and chennai, it will print
# "Both cities are in India" but if I enter mumbai and dhaka it should print "They don't belong
# to same country"
def two_city_name():
    city_1=input("city_1:")
    city_2=input("city_2:")
    if city_1 in india and city_2 in india:
        print(f"{city_1} and {city_2} both are in india")
    elif city_1 in pakistan and city_2 in pakistan:
        print(f"{city_1} and {city_2} both are in pakistan")
    elif city_1 in bangladesh and city_2 in bangladesh:
        print(f"{city_1} and {city_2} both are in bangladesh")
    else:
        print(f"{city_1} and {city_2} both are not in a single country")

## Exercise: Python If Condition
# 2. Write a python program that can tell you if your sugar is normal or not. Normal fasting level
# sugar range is 80 to 100.
#     1. Ask user to enter his fasting sugar level
#     2. If it is below 80 to 100 range then print that sugar is low
#     3. If it is above 100 then print that it is high otherwise print that it is normal
def sugar_tast():
    sugar=input("Please enter your fasting sugar level:")
    sugar=float(sugar)
    if sugar<80:
        print(f"suhar lavel {sugar} is low")
    elif sugar>=80 and sugar<=100:
        print(f"sugar lavel {sugar} is normal")
    else:
        print(f"sugar lavel {sugar} is high")
city_checker()
two_city_name()
sugar_tast()
    
