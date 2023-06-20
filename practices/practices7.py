#Third Maximum Number
#Given an integer array nums, return the third distinct maximum number in this array.
#If the third maximum does not exist, return the maximum number.
def thirdMax(nums):
    liste = []
    for i in nums:
        if i not in liste:
            liste.append(i)
    liste.sort()
    if len(liste) > 2:
        return liste[-3]
    else:
        return max(liste)

#Case
nums = [3,2,1]
########################################################################################
#Add Strings
#Given two non-negative integers, num1 and num2 represented as string, return the sum of num1 and num2 as a string.
#You must solve the problem without using any built-in library for handling large integers (such as BigInteger).
#You must also not convert the inputs to integers directly.
#Solution1
def addStrings(self, num1: str, num2: str) -> str:
    num = str(int(num1) + int(num2))
    return num

#Solution2
def addStrings(num1, num2):
    def func(n):
        value = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
        result = 0
        for digit in n:
            result = 10 * result + value[digit]
        return result
    ans = func(num1) + func(num2)
    return str(ans)

num1 = "11"
num2 = "123"

###################################################################################################
#Number of Segments in a String
#Given a string s, return the number of segments in the string.
#A segment is defined to be a contiguous sequence of non-space characters.
#Solution
def countSegments(s):
    return (len(s.split()))

s ="Hello, my name is John"

###################################################################################################
#Find All Numbers Disappeared in an Array
#Given an array nums of n integers where nums[i] is in the range [1, n], return an array of all the integers
#in the range [1, n] that do not appear in nums.
#Solution
def findDisappearedNumbers(nums):
    full_list = [i for i in range(1, len(nums) + 1)]
    return list(set(full_list) - set(nums))

nums = [1, 2, 3, 3, 4, 8, 7]
###################################################################################################