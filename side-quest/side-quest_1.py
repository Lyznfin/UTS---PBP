#pyramid, lol
n: int = 21
for i in range(n):
    j = n + i
    k = n
    while j >= 0:
        if j <= i  or i > k - 1:
            print('*', end='')
        else:
            print(' ', end='')
        j-=1
        k-=1
    print('')