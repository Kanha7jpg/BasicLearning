text = input("Enter text: ")
# Remove spaces and convert to lowercase
text = text.replace(" ", "").lower()

if text == text[::-1]:
    print("Palindrome")
else:
    print("Not a palindrome")