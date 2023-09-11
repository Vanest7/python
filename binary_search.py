#!/usr/bin/python3

list = [36, 87, 125, 18, 1, 9756, 5, 43, 981, 7, 12, 27, 915, 4938, 55]

def binary_searh(list, item):
# The list must be in order
    list.sort()
    left = 0
    right = len(list)-1
 
    while left<=right:
        middle=(left+right)//2
        if list[middle] == item:
            return middle
        elif list[middle] < item:
            left = middle + 1
        else:
            right = middle - 1
    
    return -1        

if __name__ == '__main__':
    
    print("Please, enter the number you want to search for in the list:")
    item = int(input()) 
    index_number = binary_searh(list, item) 
    if index_number == -1:
        print("The number entered is not in the list")
    else:
        print(f"The number entered is in the position: {index_number}")    