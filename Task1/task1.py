
def sequence(n: int):
    i = 1
    count = 0
    while count<n:
        for j in range(i):
            if count<n:
                print(i, end='')
                count+=1

        i+=1
n = int(input("Введите число n: "))
sequence(n)
