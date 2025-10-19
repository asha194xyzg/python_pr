"""
Simple Bank Account Management System with:
- SQLite persistence
- Authentication (PIN hashed)
- Transaction history
- Interest calculation
- Loan management
- CLI interface
"""
import sqlite3
import hashlib
import getpass
import datetime
import sys

DB="Bank.db"

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def now_str():
    return datetime.datetime.now().isoformat(timespec="seconds") + "z"

class BankDB:
    def __init__(self,db_path=DB):
        self.corr=sqlite3.connect(db_path,check_same_thread=False)
        self._create_tables()
    def _create_tables(self):
        cur=self.corr.cursor()
        
        cur.execute("""create table if not exists accounts(
            id integer primary key autoincrement,
            account_no text unique,
            name text,
            pin_hash text,
            balance real default 0.0,
            created_at text)
                    """)
        
        cur.execute("""create table if not exists transactions(
            id integer primary key autoincrement,
            account_no text,
            type text,
            amount real,
            balance_after real,
            timestamp text,
            note text
            
        )
        """)
        
        cur.execute("""create table if not exists loans(
            id integer primary key autoincrement,
            account_no text,
            principal real,
            outstanding real,
            annual_rate real,
            created_at text
        )""")
        self.corr.commit()
        
    # Account operations
    def create_account(self,account_no,name,pin,initial_balance=0.0):
        cur=self.corr.cursor()
        pin_hash=sha256(pin)
        cur.execute("INSERT INTO accounts(account_no,name,pin_hash,balance,created_at) values (?,?,?,?,?)",
                    (account_no,name,pin_hash,initial_balance,now_str()))
        self.corr.commit()
        self.add_transactions(account_no,"CREATE_ACCOUNT",initial_balance,float(initial_balance),"ACCOUNT_CREATED")
        
    def get_account(self,account_no):
        cur=self.corr.cursor()
        cur.execute(" SELECT account_no, name, pin_hash, balance, created_at FROM accounts where account_no=?",(account_no,))
        row=cur.fetchone()
        if row:
            return {"account_id":row[0],"name":row[1],"pin_hash":row[2],"balance":row[3],"created_at":row[4]}
        return None
    def check_pin(self,account_no,pin):
        acc=self.get_account(account_no)
        if not acc:
            return False
        return sha256(pin)==acc["pin_hash"]
    
    def update_balance(self,account_no,new_balance):
        cur=self.corr.cursor()
        cur.execute("UPDATE accounts set balance=? where account_no=?",(new_balance,account_no))
        self.corr.commit()
        
    def add_transactions(self, account_no, ttype, amount, balance_after, note=""):
        cur=self.corr.cursor()
        cur.execute("INSERT INTO transactions (account_no,type,amount,balance_after,timestamp,note) VALUES(?,?,?,?,?,?)",
                    (account_no, ttype,float(amount),float(balance_after),now_str(), note))
        self.corr.commit()
        
    def get_transactions(self,account_no,limit=100):
        cur=self.corr.cursor()
        cur.execute(f"SELECT type, amount, balance_after, timestamp, note FROM transactions WHERE account_no=? ORDER BY id DESC LIMIT {limit}",(account_no,))
        rows=cur.fetchall()
        return rows
    
    # Loan operations
    
    def create_loan(self,account_no,principal,annual_rate):
        cur=self.corr.cursor()
        cur.execute("INSERT INTO loans (account_no,principal,outstanding,annual_rate,created_at) values(?,?,?,?,?)",
                    (account_no,float(principal),float(principal),float(annual_rate),now_str()))
        self.corr.commit()
    def get_loans(self,account_no):
        cur=self.corr.cursor()
        cur.execute("SELECT id, principal, outstanding, annual_rate, created_at FROM loans WHERE account_no=?",(account_no,))
        row=cur.fetchall()
        return row
    def update_loan_outstanding(self,loan_id,new_outstanding):
        cur=self.corr.cursor()
        cur.execute("UPDATE loans set outstanding=? where id=?",(float(new_outstanding),loan_id))
        self.corr.commit()
    
    def close(self):
        self.corr.close()

class Account_service:
    def __init__(self,BankDB):
        self.db=BankDB
    def create_account(self,account_no,name,pin,initial_balance=0.0):
        if self.db.get_account(account_no):
            raise ValueError("Account already exists")
        self.db.create_account(account_no,name,pin,initial_balance)
        print(f"Account {account_no} create for {name} with balance {initial_balance}TK")
        
    def get_balance(self,account_no):
        acc=self.db.get_account(account_no)
        if not acc:
            raise ValueError("Account not found.")
        return acc["balance"]
    def deposit(self,account_no,amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        acc=self.db.get_account(account_no)
        new_balance=acc["balance"]+float(amount)
        self.db.update_balance(account_no,new_balance)
        self.db.add_transactions(account_no,"DEPOSIT",amount,new_balance,"CASH_DEPOSIT")
        print(f"Deposited {amount}TK. New balance: {new_balance}TK")
         
    def withdraw(self,account_no,amount):
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive.")
        acc=self.db.get_account(account_no)
        if acc["balance"]<amount:
            raise ValueError("Insufficient balance.")
        new_balance=acc["balance"]-float(amount)
        self.db.update_balance(account_no,new_balance)
        self.db.add_transactions(account_no,"WITHDRAW",amount,new_balance,"CASH_WITHDRAW")
        print(f"Withdrew {amount}TK. New balance: {new_balance}TK")
    
    def show_transactions(self,account_no,limit=50):
        txns=self.db.get_transactions(account_no,limit)
        if not txns:
            print("No transactions found.")
            return
        print(f"Last {len(txns)} transactions for account {account_no}:")
        for txn in txns:
            type,amount,balance_after,timestamp,note=txn
            print(f"{timestamp}| {type:10} |{amount:10.2f}TK| Balance after: {balance_after:10.2f}TK| Note: {note}")

# Simple interest application: apply once for current balance using annual_rate percent, fraction_of_year in years

    def apply_interest(self,account_no,annual_rate_percent, fraction_of_year=1.0):
        acc=self.db.get_account(account_no)
        if not acc:
            raise ValueError("Account not found")
        
        principal=acc["balance"]
        interest=principal*(float( annual_rate_percent))*(float(fraction_of_year))
        new_balance=principal+interest
        self.db.update_balance(account_no,new_balance)
        self.db.add_transactions(account_no, "INTEREST", interest, new_balance, f"Interest : {annual_rate_percent}% for {fraction_of_year} year(s)")
        
        print(f"Interest {interest:.2f} Tk applied. New balance: {new_balance:.2f} Tk")
        
    # Loan functions
    def take_loan(self,account_no,principal,annual_rate_percent):
         # add loan record, credit principal to account balance
         self.db.create_loan(account_no,principal,annual_rate_percent)
         self.deposit(account_no,principal)
         self.db.add_transactions(account_no,"LOAN_TAKEN",principal,self.get_balance(account_no),f"Loan : {annual_rate_percent}% p.a.")
         print(f"Loan of {principal} Tk created for account {account_no} at {annual_rate_percent}% p.a.")
    
    def list_Loans(self,account_no):
        loans=self.db.get_loans(account_no)
        if not loans:
            print("No loan for this account")
            return
        print("Loans")
        for loan in loans:
            loan_id,principal,outstanding,annual_rate,created_at=loan
            print(f"ID: {loan_id}, Principal: {principal}, Outstanding: {outstanding}, Annual Rate: {annual_rate}%, Created At: {created_at}")
            
    def repay_loan(self,account_no,loan_id,amount):
        # pay from account balance towards loan outstanding
        acc=self.db.get_account(account_no)
        if acc["balance"]<amount:
            raise ValueError("Insufficient balance to repay loan.")
        loans=self.db.get_loans(account_no)
        loan=next((l for l in loans if l[0]==loan_id), None)
        if not loan:
            raise ValueError("Loan not found.")
        outstanding=loan[2]
        pay=min(amount,outstanding)
        new_outstanding=outstanding-pay
        # debit account balance
        self.withdraw(account_no,pay)
        # update loan outstanding
        self.db.update_loan_outstanding(loan_id,new_outstanding)
        self.db.add_transactions(account_no,"LOAN_REPAYMENT",pay,self.get_balance(account_no),f"Loan ID {loan_id} repayment")
        print(f"Repaid {pay:.2f} Tk towards loan ID {loan_id}. New outstanding: {new_outstanding:.2f} Tk")
        
  # Simple loan interest accrual (adds interest to outstanding): interest = outstanding * rate * fraction_of_year 
    def accrue_loan_interest(self,account_no,loan_id,fraction_of_year=1.0):
        cur=self.db.corr.cursor()
        cur.execute("SELECT account_no,outstanding,annual_rate FROM loans WHERE id=?",(loan_id,))
        row=cur.fetchone()
        if not row:
            raise ValueError("Loan not found.")
        account_no,outstanding,annual_rate=row
        interest=outstanding*(float(annual_rate)/100.0)*(float(fraction_of_year))
        new_outstanding=outstanding+interest
        self.db.update_loan_outstanding(loan_id,new_outstanding)
        self.db.add_transactions(account_no,"LOAN_INTEREST",interest,self.get_balance(account_no),f"Loan ID {loan_id} interest accrual")
        print(f"Accrued {interest:.2f} Tk interest on loan ID {loan_id}. New outstanding: {new_outstanding:.2f} Tk")
        
def input_pin(prompt="Enter PIN: "):
        # use getpass so PIN not shown
        return getpass.getpass(prompt)

def main_cli():
    db=BankDB()
    service=Account_service(db)

    print("___Simple Bank System___")

    while True:
        print("\nOptions:")
        print("1. Create Account")
        print("2. Login to Account")
        print("3. Exit")
        choice=input("Select an option: ")
        if choice=="1":
            account_no=input("Enter account number:").strip()
            name=input("Enter account holder name:").strip()
            pin=input_pin("Set 4-6 digit PIN: ")
            pin_confirm=input_pin("Confirm PIN: ")
            if pin!=pin_confirm:
                print("PINs do not match.")
                continue
            try:
                initial=float(input("Initial deposit amount(0 if none)): ") or 0.0)
            except ValueError:
                print("Invalid amount.")
                continue
            try:
                service.create_account(account_no,name,pin,initial)
            except Exception as e:
                print(f"Error: {e}")
                    
        elif choice=="2":
            account_no=input("Enter account number:").strip()
            if not db.get_account(account_no):
                print("Account not found.")
                continue
                
            pin=input_pin("Enter PIN: ")
            if not db.check_pin(account_no,pin):
                print("Invalid PIN.")
                continue
            print(f"Login successful for account {account_no}.")
            # Logged in menu
                
            print(f"\nWelcome, {account_no}!")
                
            while True:
                print("\nAccount Options:")
                print("1. Show Balance")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. Show Transactions")
                print("5. Take Loan")
                print("6. List Loans")
                print("7. Repay Loan")
                print("8. Apply Interest to Balance (simple)")
                print("9. Accrue Loan Interest (simple)")
                print("0. Logout")
                opt=input("choose: ").strip()
                try:
                    if opt=="1":
                        balance=service.get_balance(account_no)
                        print(f"Current balance: {balance:.2f} Tk")
                    elif opt=="2":
                        amt=float(input("Enter deposit amount: "))
                        service.deposit(account_no,amt)
                    elif opt=="3":
                        amt=float(input("Enter withdraw amount: "))
                        service.withdraw(account_no,amt)
                    elif opt=="4":
                        service.show_transactions(account_no,limit=50)
                    elif opt=="5":
                        principal=float(input("Enter loan principal amount: "))
                        rate=float(input("Enter annual interest rate (%): "))
                        service.take_loan(account_no,principal,rate)
                    elif opt=="6":
                        service.list_Loans(account_no)
                    elif opt=="7":
                        loan_id=int(input("Enter loan ID to repay: "))
                        amt=float(input("Enter repayment amount: "))
                        service.repay_loan(account_no,loan_id,amt)
                            
                    elif opt=="8":
                        rate=float(input("Enter annual interest rate (%): "))
                        months=float(input("Enter fraction of year (e.g., 1.0 for full year and 0.0833 for one month): ") or 1.0)
                        service.apply_interest(account_no,rate,months)
                    elif opt=="9":
                        service.list_Loans(account_no)
                        loan_id=int(input("Enter loan ID to accrue interest: "))
                        fraction=float(input("Enter fraction of year (e.g., 1.0 for full year and 0.0833 for one month): ") or 1.0)
                        service.accrue_loan_interest(account_no,loan_id,fraction)
                    elif opt=="0":
                        print("Logging out.")
                        break
                    else:
                        print("Invalid option.")
                except Exception as e:
                    print(f"Error: {e}")
        
        elif choice=="3":
            print("Exiting. Goodbye!")
            db.close()
            sys.exit(0)
        else:
            print("Invalid option,try again.")
                
if __name__=="__main__":
        main_cli()
                