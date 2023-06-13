from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

# Khởi tạo cặp khóa
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# Lưu khóa vào file
with open("data/private_key.pem", "wb") as f:
    f.write(private_key)

with open("data/public_key.pem", "wb") as f:
    f.write(public_key)

# Mã hóa và giải mã một thông điệp
MESSAGE = b"Hello, world!"
cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
encrypted_message = cipher.encrypt(MESSAGE)

cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
decrypted_message = cipher.decrypt(encrypted_message)

print(decrypted_message.decode())
