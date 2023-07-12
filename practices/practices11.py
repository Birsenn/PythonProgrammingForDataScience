########################################################################################
#Reverse Array in Groups
#Given an array arr[] of positive integers of size N. Reverse every sub-array group of size K.
#Note: If at any instance, there are no more subarrays of size greater than or equal to K, then reverse the last
#subarray (irrespective of its size). You shouldn't return any array, modify the given array in-place.
def reverseInGroups(arr, N, K):


#Input:
#N = 5, K = 3
#arr[] = {1,2,3,4,5}
#Output: 3 2 1 5 4
#Explanation: First group consists of elements 1, 2, 3. Second group consists of 4,5.

########################################################################################
#Longest Consecutive Sequence
#Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.
#You must write an algorithm that runs in O(n) time.
def longestConsecutive(nums):
    nums = list(set(nums))
    nums = sorted(nums)
    counter = 1
    counter_list = []

    if len(nums) == 0: #early return
        return 0
    if len(nums) == 1: #early return
        return 1
    if len(nums) > 1:
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1] + 1:
                counter += 1
                counter_list.append(counter)
            else:
                counter_list.append(counter)
                counter = 1
        return max(counter_list)


########################################################################################
