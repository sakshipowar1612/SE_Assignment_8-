n = int(input("Enter a number(not equal to 1): "))
for i in range(2, n):
    if n==2:
        print('Prime')
        break
    elif n%i == 0:
        print('Not Prime')
        break
else:
    print('Prime')