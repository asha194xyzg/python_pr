class Book:
    def __init__(self,title,author,isbn,publication):
        self.title=title
        self.author=author
        self.isbn=isbn
        self.publication=publication
        self.is_available=True   
    def show(self):
        print(f"{self.title} by {self.author} (ISBN:{self.isbn})-{"Avaiable" if self.is_available else "Borrowed"} and Publication by {self.publication}")
        
class Member:
    def __init__(self,name,member_Id):
        self.name=name
        self.member_id=member_Id
        self.borrowed_books=[]
    def borrow_book(self, book):
        if book.is_available:
            self.borrowed_books.append(book) 
            book.is_available = False       
            print(f"{self.name} borrowed '{book.title}'")
        else:
            print(f"Sorry, '{book.title}' is not available")
        

    def return_book(self,book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            self.is_available=True
            print(f"{self.name} returned {book.title}")
        else:
            print(f"{self.name} did not borrow {book.title}")
    # Library class
    
class Library:
    def __init__(self,name):
        self.name=name
        self.books=[]
        self.members=[]
    def add_book(self,book):
        self.books.append(book)
        print(f"Book {book.title} added to library.")
    def add_member(self,member):
        self.members.append(member)
        print(f"member {member.name} added to library.")
    def show_books(self):
        print("\nLibrary books:")
        for book in self.books:
            print(list(book.title))
    
    def show_members(self):
        print("\nLibrary members:")
        for member in self.members:
            print(f"{member.name} (ID: {member.member_id})")
    
book1 = Book("পাথরের দেবী", "হুমায়ূন আহমেদ", "978-984-70120-5-3", "অনন্যা")
book2 = Book("শঙ্খনীল কারাগার", "হুমায়ূন আহমেদ", "978-984-412-123-4", "অনন্যা")
book3 = Book("লালসালু", "সেলিনা হোসেন", "978-984-70220-7-5", "সময় প্রকাশনী")
book4 = Book("কাকের খাবার", "সেলিনা হোসেন", "978-984-501-555-6", "সময় প্রকাশনী")
book5 = Book("দেবদাস", "শরৎচন্দ্র চট্টোপাধ্যায়", "978-984-455-987-0", "প্রথমা প্রকাশন")
book6 = Book("গীতাঞ্জলি", "রবীন্দ্রনাথ ঠাকুর", "978-984-111-222-3", "বিশ্বভারতী প্রকাশনী")
book7 = Book("কবিতা সমগ্র", "জীবনানন্দ দাশ", "978-984-333-444-5", "কাকলী প্রকাশনী")
book8 = Book("সূর্য দীঘল বাড়ি", "আবু ইসহাক", "978-984-888-999-1", "আনন্দ প্রকাশন")
book9 = Book("মধ্যরাতে ঢাকা", "সেলিনা হোসেন", "978-984-541-777-2", "সময় প্রকাশনী")
book10 = Book("মহাশূন্যের অতিথি", "হুমায়ূন আহমেদ", "978-984-112-333-9", "অনন্যা")
books=[book1,book2,book3,book4,book5,book6,book7,book8,book9,book10]
library=Library("City Library")
for book in books:
    library.add_book(book)
book.show()
library.show_books()
member1 = Member("Asha", 1)
member2 = Member("Rafiq", 2)
member3 = Member("Nusrat", 3)
member4 = Member("Sabbir", 4)
member5 = Member("Mitu", 5)
member6 = Member("Karim", 6)
member7 = Member("Faria", 7)
member8 = Member("Tanvir", 8)
member9 = Member("Sumaiya", 9)
member10 = Member("Jamal", 10)
members = [member1, member2, member3, member4, member5, 
           member6, member7, member8, member9, member10]
for member in members:
    library.add_member(member)
    
member4.borrow_book(book3)
member6.borrow_book(book10)
member7.borrow_book(book3)
member4.return_book(book6)
library.show_members()

