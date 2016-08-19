# Cheking palindrome
test_string = "configifnoc"
test_string = test_string.casefold()
revers_str = reversed(test_string)
if list(test_string) == list(revers_str):
 print("the string is a palindrome")
else:
 print("the string is not a palindrome")