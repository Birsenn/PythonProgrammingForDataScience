import timeit

#Contains Duplicate II
def containsNearbyDuplicate(nums, k):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j] and abs(i - j) <= k:
                return True

#this function is ture but time limit exceed so we can use below function - hashmap method (50 ms)
def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
    seen = {}
    for i in range(len(nums)):
        if nums[i] in seen and i - seen[nums[i]] <= k:
            return True
        seen[nums[i]] = i
    return False

nums = [1,2,3,1]
k = 3
###############################################################
#Missing Number
def missingNumber(nums):
    nums.sort()
    for i in range(len(nums)):
        if i != nums[i]:
            return i
    return nums[-1] + 1

nums = [9,6,4,2,3,5,7,0,1]

###############################################################
#Single Number
def singleNumber(nums):
    keep = []
    for i in nums:
        if i not in keep:
            keep.append(i)
        else:
            del i in keep #bunu nasıl diyebilirim? keep listesinin içindeki i yi silmek istiyorum
    return keep

#True solution
def singleNumber(nums):
    keep = {}
    for i in nums:
        if i not in keep:
            keep[i] = 1
        else:
            del keep[i]
    return keep.keys() #normalde liste dönmesi için list(keep.keys()) olması lazım ama çalışmıyor sebebini anlamadım???

nums = [1, 1, 2, 3, 3, 4, 5, 5]


#deneme
myDict = {'a': 'apple', 'b': 'banana', 'c': 'cherry'}
liste = list(myDict.keys()) #TypeError: 'list' object is not callable ???
