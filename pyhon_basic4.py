

# We have following information on countries and their population (population is in crores),

# Country	Population
# China	143
# India	136
# USA	32
# Pakistan	21
# Using above create a dictionary of countries and its population
# Write a program that asks user for three type of inputs,
# print: if user enter print then it should print all countries with their population in this format,
# china==>143
# india==>136
# usa==>32
# pakistan==>21
# add: if user input add then it should further ask for a country name to add. If country already exist in our dataset then it should print that it exist and do nothing. If it doesn't then it asks for population and add that new country/population in our dictionary and print it
# remove: when user inputs remove it should ask for a country to remove. If country exist in our dictionary then remove it and print new dictionary using format shown above in (a). Else print that country doesn't exist!
# query: on this again ask user for which country he or she wants to query. When user inputs that country it will print population of that country.
country_population={
    "chaina":143,
    "india":136,
    "usa":32,
    "pakistan":21
}
print("Welcome to the Country Population Program!",country_population)
for country, population in country_population.items():
    print(f"{country}==>{population}")
def add():
    country=input("Enter country name to add: ").lower()
    if country in country_population:
        print(f"{country} already exists in the dataset.")
        return
    population = input(f"Enter population for {country}: ")
    population = int(population)
    country_population[country] = population
    print(f"{country} added with population {population}.")
    print_all()
def remove():
    country = input("Enter country name to remove: ").lower()
    if country in country_population:
        del country_population[country]
        print(f"{country} removed from the dataset.")
    else:
        print(f"{country} doesn't exist in the dataset.")
    print_all()
    
def query():
    country = input("Enter country name to query: ").lower()
    if country in country_population:
        print(f"Population of {country} is {country_population[country]}.")
    else:
        print(f"{country} doesn't exist in the dataset.")
def print_all():
    for country,population in country_population.items():
        print(f"{country}==>{population}")
        
def main():
    op=input("Enter operation (add,remove,query or print): ").lower()
    if op == "add":
        add()
    elif op == "remove":
        remove()
    elif op == "query":
        query()
    elif op == "print":
        print_all()
if __name__ == "__main__":
    main()
    

    
        
        
            