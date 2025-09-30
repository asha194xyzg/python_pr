class Account:
    def __init__(self,bal,acc):
        self.balance=bal
        self.account=acc
    def debit(self,amount):
        self.balance-=amount
        print(f"{amount}Tk was debited")
        print(f" Current balance is:{self.get_balance()}")
    def credit(self,amount):
        self.balance+=amount
        print(f"{amount}Tk was credited")
        print(f"Current balanc is:{self.get_balance()}")
    def get_balance(self):
        return self.balance
        
c1=Account(1500000,247688)
c1.debit(20000)
c1.credit(50000)
