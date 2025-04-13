with open('message.txt', 'r', encoding='utf-8') as file_in:
    content = file_in.read()

binary_content = ' '.join(format(ord(char), '08b') for char in content)


with open('messagenhiphan.txt', 'w', encoding='utf-8') as file_out:
    file_out.write(binary_content)

print("Da chuyen noi dung sang nhi phan va luu vao messagenhiphan.txt")
