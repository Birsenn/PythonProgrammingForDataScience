########################################################################################
#Valid Parenthesis
#Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
#An input string is valid if:
#Open brackets must be closed by the same type of brackets.
#Open brackets must be closed in the correct order.
#Every close bracket has a corresponding open bracket of the same type.

def isValid(self, s: str) -> bool:
    while "()" in s or "[]" in s or "{}" in s:
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return False if len(s) != 0 else True

########################################################################################
#Majority Element
#Given an array nums of size n, return the majority element.
#The majority element is the element that appears more than ⌊n / 2⌋ times.
#You may assume that the majority element always exists in the array.

def majorityElement(nums):
    sozluk = {}
    for i in nums:
        if i not in sozluk:
            sozluk[i] = 1
        else:
            sozluk[i] += 1
    for j in sozluk:
        if sozluk[j] > len(nums) / 2:
            return j
#tek seferde:)

########################################################################################
#Happy Number
#Write an algorithm to determine if a number n is happy.
#A happy number is a number defined by the following process:
#Starting with any positive integer, replace the number by the sum of the squares of its digits.
#Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
#Those numbers for which this process ends in 1 are happy.
#Return true if n is a happy number, and false if not.

def isHappy(29):
    n = str(n)
    l = []
    while n != "1":
        new_n = 0
        for i in n:
            new_n += (int(i)**2)
        if new_n in l:
            return False
        l.append(new_n)
        n = str(new_n)
    return True

########################################################################################
#Find Smallest Letter Greater Than Target
#You are given an array of characters letters that is sorted in non-decreasing order, and a character target.
#There are at least two different characters in letters.
#Return the smallest character in letters that is lexicographically greater than target. If such a character does not exist,
#return the first character in letters.

def nextGreatestLetter(letters, target):
    for i in letters:
        if target != i and sorted([target, i])[1] == i:
            return i
    return letters[0]

########################################################################################
