#Palindrome Number
#condition: without converting the integer to a string

def isPalindrome(x):
    if x < 0 or (x != 0 and x % 10 == 0):
        return False

    half = 0
    while x > half:
        half = (half * 10) + (x % 10)
        x = x // 10
    return x == half or x == half // 10

##########################################################
#Valid Anagram
def isAnagram(s, t):
    if sorted(s) == sorted(t):
        return True
    else:
        return False

#example:
#Input: s = "anagram", t = "nagaram"
#Output: true

##########################################################
#Remove Duplicates from Sorted Array
def removeDuplicates(nums):
    j=1
    for i in range(1, len(nums)):
        if nums[i] != nums[i-1]:
            nums[j] = nums[i]
            j += 1
    return j

list = [1,1,2,3,3,4,5]
removeDuplicates(list)

##########################################################
#Remove Element
def removeElement(nums, val):
    while val in nums:
        nums.remove(val)
    return len(nums)

removeElement(list, 3)

##########################################################
#Two Sum
def twoSum(nums, target):
    output_list = []
    for a in range(len(nums)):
        for b in range(a + 1, len(nums)):
            if (nums[a] + nums[b] == target):
                output_list.append(a)
                output_list.append(b)
                break
            else:
                continue
    return output_list

###########################################################
#Contains Duplicate
def containsDuplicate(nums):
    return len(set(nums)) != len(nums)

#example
#Input: nums = [1,2,3,1]
#Output: true

#Input: nums = [1,2,3,4]
#Output: false

###########################################################