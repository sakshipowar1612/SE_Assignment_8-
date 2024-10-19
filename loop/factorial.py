def fact(num):
    ans = 1
    for i in range(1,num+1):
        ans=ans*i
    return ans

num = int(input("Enter a number: "))
print(fact(num))