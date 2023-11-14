#https://thecleverprogrammer.com/2021/04/22/merge-sort-using-python/

def merge(listA, listB):
    newlist = []
    a=0
    b=0
    while a<len(listA) and b < len(listB):
        if listA[a]<listB[b]:
                newlist.append(listA[a])
                a+= 1
        else:
            newlist.append(listB[b])
            b+=1
        
    while a<len(listA):
        newlist.append(listA[a])
        a+=1
        
    while b<len(listB):
        newlist.append(listB[b])
        b+=1
    return newlist
    
def merge_sort(input_list):
    if len(input_list)<=1:
        return input_list
    else:
        mid=len(input_list)//2
        left= merge_sort(input_list[:mid])
        right= merge_sort(input_list[mid:])
        newlist=merge(left,right)
        return newlist


a = [3, 7, 2, 9, 11, 5]
print("Original List (a):", a)
print("Sorted List (a):", merge_sort(a))
print()

b = [1, 8, 6, 14, 12, 9, 2]
print("Original List (b):", b)
print("Sorted List (b):", merge_sort(b))
print()

c = [10, 4, 8, 6, 13, 11, 7, 15]
print("Original List (c):", c)
print("Sorted List (c):", merge_sort(c))
print()

d = [5, 9, 12, 3, 6, 14]
print("Original List (d):", d)
print("Sorted List (d):", merge_sort(d))
print()

e = [7, 13, 2, 10, 11]
print("Original List (e):", e)
print("Sorted List (e):", merge_sort(e))
print()

f = [4, 12, 15, 1, 3, 9, 5, 8]
print("Original List (f):", f)
print("Sorted List (f):", merge_sort(f))
print()

g = [11, 2, 6, 14, 7, 13]
print("Original List (g):", g)
print("Sorted List (g):", merge_sort(g))
print()

h = [9, 5, 3, 1, 12, 8]
print("Original List (h):", h)
print("Sorted List (h):", merge_sort(h))
print()

i = [6, 14, 9, 4]
print("Original List (i):", i)
print("Sorted List (i):", merge_sort(i))
print()

j = [2, 8, 10, 3, 12, 6, 13]
print("Original List (j):", j)
print("Sorted List (j):", merge_sort(j))