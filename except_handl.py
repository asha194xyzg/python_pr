def fuction():
    try:
        l=[2,5,7,8,4,9]
        a=int(input("enter the index :"))
        print(l[a])
        return 1
    except:
        print("some error occurred")
        return 0
    finally:
        print("I am always executed")
x=fuction()
print(x)