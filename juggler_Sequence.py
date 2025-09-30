import math

def jugglerSequence(n):
    seq = [n] 
    print(seq)
  
    while n != 1:
        if n % 2 == 0:   
            n = int(math.sqrt(n))
        else:            
            n = int(n ** 1.5)   # n^(3/2)
        seq.append(n)
    
    return seq
print(jugglerSequence(9))