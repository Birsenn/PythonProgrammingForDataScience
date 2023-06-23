#######################################################################################
#Lemonade Change
#At a lemonade stand, each lemonade costs $5. Customers are standing in a queue to buy from you and order one at a time (in the order
#specified by bills). Each customer will only buy one lemonade and pay with either a $5, $10, or $20 bill. You must provide the correct
#change to each customer so that the net transaction is that the customer pays $5.
#Note that you do not have any change in hand at first.
#Given an integer array bills where bills[i] is the bill the ith customer pays, return true if you can provide every customer with the
#correct change, or false otherwise.
#Solution
def lemonadeChange(bills):
    changes = {5:0, 10:0}

    for i in bills:
        if i == 5:
            changes[5] += 1
        elif i == 10:
            if changes[5] ==0:
                return False
            changes[5] -= 1
            changes[10] += 1
        elif i ==20:
            if changes[10] >0 and changes[5] > 0:
                changes[5] -= 1
                changes[10] -= 1
            elif changes[5] >2:
                changes[5] -= 3
            else:
                return False
    return True
bills = [5,5,5,10,20]


#######################################################################################
#Missing Number in Array
#Given an array of size N-1 such that it only contains distinct integers in the range of 1 to N. Find the missing element.
#Input:
#N = 5
#A[] = {1,2,3,5}
#Output: 4
#Solution
def missingNumber(array, n):
    return int(n*(n+1)/2 - sum(array))

#######################################################################################
#Prefix match with other strings
#Given an array of strings arr[] of size n, a string str and an integer k. The task is to find the count of strings in arr[]
#whose prefix of length k matches with the k-length prefix of str.
def klengthpref(arr, n, k, s):
    if len(s) < k:
        return 0

    str = s[0:k]
    count = 0
    for i in arr:
        if str == i[0:k]:
            count += 1
    return count

#Example
#arr = ["abba", "abbb", "abbc", "abbd", "abaa", "abca"]
#s = "abbg"
#n = 6
#k = 3

#######################################################################################