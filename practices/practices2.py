#Best Time to Buy and Sell Stock
def maxProfit(prices):
    minPrice, maxProfit = float('inf'), 0
    for price in prices:
        if price < minPrice:
            minPrice = price
        elif price - minPrice > maxProfit:
            maxProfit = price - minPrice
    return maxProfit

prices = [7,1,5,3,6,4],
maxProfit(price)

#note:"inf" represent a infinite integer

#########################################################
#Longest Common Prefix
def longestCommonPrefix(strs):
    if len(strs) == 0:
        return ""

    base = strs[0]
    for i in range(len(base)):
        for word in strs[1:]:
            if i == len(word) or word[i] != base[i]:
                return base[0:i]
    return base

strs =["flower","flow","flight"]
strs =["a","ağız","ağıt"]
longestCommonPrefix(strs)

#########################################################
#Valid Palindrome
def isPalindrome(s):
    s = "".join(c for c in s if c.isalnum()).lower()
    return s == s[::-1]

s ="A man, a plan, a canal: Panama"
s ="race a car"

#########################################################
#Remove Dublicates from Sorted List
def deleteDuplicates(lst):
    lst = sorted(lst)
    new_lst = []
    for i in range(len(lst)):
        if lst[i] not in lst[:i]:
            new_lst.append(lst[i])
    return new_lst
list = [1, 1, 2, 3, 5, 2, 2]

deleteDuplicates(list)

########################################################


