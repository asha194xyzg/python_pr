# ## Exercise: Python for loop
# 1. After flipping a coin 10 times you got this result,
# ```
# result = ["heads","tails","tails","heads","tails","heads","heads","tails","tails","tails"]
# ```
# Using for loop figure out how many times you got heads
print("\nExercise 1\n")
result = ["heads","tails","tails","heads","tails","heads","heads","tails","tails","tails"]
count=0
for itam in result:
    if itam=="heads":
        count+=1
print("head count:",count)

for i in range(1,11):
    if i%2==0:
        continue
    print(i*i)

