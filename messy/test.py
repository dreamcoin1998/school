import random
random.randint
def main():
    n = int(input())
    count = 0
    bianDic = {}
    while count < n * 6:
        if count % 6 == 0 and count != 0:
            # print(bianDic.values())
            if set(bianDic.values()) == set([4, 4, 4]) or set(bianDic.values()) == set([4, 8]) or set(bianDic.values()) == set([12]):
                print('POSSIBLE')
            else:
                print('IMPOSSIBLE')
            bianDic = {}
        l1, l2 = input().split(' ')
        if bianDic.get(l1):
            bianDic[l1] += 1
        else:
            bianDic[l1] = 1
        if bianDic.get(l2):
            bianDic[l2] += 1
        else:
            bianDic[l2] = 1
        count += 1
    if set(bianDic.values()) == set([4, 4, 4]) or set(bianDic.values()) == set([4, 8]) or set(bianDic.values()) == set([12]):
        print('POSSIBLE')
    else:
        print('IMPOSSIBLE')
main()
