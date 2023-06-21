#Reverse Coding
#You will be given an integer n, your task is to return the sum of all natural number less than or equal to n.
#As the answer could be very large, return answer modulo 10üzeri9+7.
def sumOfNaturals(n):
    summ = 0
    summ = int(n * (n + 1) / 2)
    return summ % 1000000007

########################################################################################
#Binary Search
#Given a sorted array of size N and an integer K, find the position(0-based indexing) at which K is present in the array using binary search.
def binarysearch(arr, n, k):
    for i in range(0,n):
	        if k == arr[i]:
		        return i
	return -1

arr = [1,2, 3, 4, 5]
n = 5
k = 4

########################################################################################
#Check if two arrays are equal or not
#Given two arrays A and B of equal size N, the task is to find if given arrays are equal or not. Two arrays are said to be equal if both of them contain same set of elements, arrangements (or permutation) of elements may be different though.
#Note : If there are repetitions, then counts of repeated elements must also be same for two array to be equal.
def check(A,B,N):
        A.sort()
        B.sort()
        return A==B

########################################################################################
#Given an array of N integers. Find the first element that occurs at least K number of times.
#Input :
#N = 7, K = 2
#A[] = {1, 7, 4, 3, 4, 8, 7}
#Output : 4 #first occurance
def firstElementKTime(a, n, k):
    count = {}
    for i in a:
        if i not in count:
            count[i] = 1
        else:
            count[i] += 1

        if count[i] == k:
            return i
    return -1

########################################################################################
