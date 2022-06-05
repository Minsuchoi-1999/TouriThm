#!/usr/bin/python

def quick_sort_ascending(array):
    if len(array) <= 1:
        return array

    pivot = array[0] 
    tail = array[1:] 

    left_side = [x for x in tail if x <= pivot] 
    right_side = [x for x in tail if x > pivot]

    return quick_sort_ascending(left_side) + [pivot] + quick_sort_ascending(right_side)

def quick_sort_descending(array):
    if len(array) <= 1:
        return array

    pivot = array[0] 
    tail = array[1:] 

    left_side = [x for x in tail if x > pivot] 
    right_side = [x for x in tail if x <= pivot]

    return quick_sort_descending(left_side) + [pivot] + quick_sort_descending(right_side)


print("input numbers to sort")
array=list(map(int,input().split()))

if input("ascending or descneding? (a/d) ")=="a":
    print(quick_sort_ascending(array))
else:
    print(quick_sort_descending(array))