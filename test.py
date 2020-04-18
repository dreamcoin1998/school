n=eval(input())
for i in range(1,2*n):
    if i%2==1:
        print((i*"*").center(2*n-1))
    else:
        print()
print()
for i in range(1,2*n-1):
    if i%2==1:
        print(((2*n-2-i)*"*").center(2*n-1).rstrip())
    else:
        print()