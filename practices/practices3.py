#Merge Sorted Array
def merge(nums1, nums2):
    for x in nums2:
        if 0 in nums1:
            nums1.remove(0)
            nums1.append(x)
            nums1.sort()
    return nums1

###########################################
#Length of Last Word
def lengthOfLastWord(s):
    list = s.split()
    return len(list[-1])

s = "It is a beautiful day"

#######################################################
#Plus One
def plusOne(digits):
    strings = ""
    for number in digits:
        strings += str(number)

    temp = str(int(strings) + 1)

    return [int(temp[i]) for i in range(len(temp))]

########################################################
#Sqrt(x)
def mySqrt(x):
    if x == 0:
        return 0
    if x == 1:
        return 1
    for i in range(1, x + 1):
        if i * i > x:
            return i - 1

mySqrt(105)

########################################################
