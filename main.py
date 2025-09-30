class Student:
    def __init__(self,name,Roll,marks):
        self.name=name
        self.Roll=Roll
        self.marks=marks
    def get_avg(self):
        sum=0
        for i in self.marks:
            sum=sum+i
            avg=sum/len(self.marks)
            
        print(f"Hi,My name is {self.name} ,my roll is {self.Roll},my total marks in exam is {avg}")
s1=Student("Asha Alin",10,[98,96,97,90,95])
s1.get_avg()
        
    

    

    