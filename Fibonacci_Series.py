
class Solution:
    def series(self, n):
        modula=10**9+7
        if n==0:
            return [0]
        if n==1:
            return [0,1]
        fib=[0]*(n+1)
        fib[0],fib[1]=0,1
        for i in range(2,n+1):
            fib[i]=(fib[i-1]+fib[i-2])% modula
            
        return fib
c=Solution()
print(c.series(10))