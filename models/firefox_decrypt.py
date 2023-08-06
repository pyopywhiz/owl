import hmac
import os
import sqlite3
from base64 import b64decode
from binascii import unhexlify
from hashlib import pbkdf2_hmac, sha1
from struct import unpack
from typing import Any, Dict

from Crypto.Cipher import AES, DES3
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
from pyasn1.codec.der import decoder


def get_short_le(data: bytes, index: int) -> Any:
    return unpack("<H", data[index: index + 2])[0]


def get_long_be(data: bytes, index: int) -> Any:
    return unpack(">L", data[index: index + 4])[0]


def read_bsddb(filename: str) -> Dict[bytes, bytes]:
    with open(filename, "rb") as file:
        header = file.read(4 * 15)
        page_size = get_long_be(header, 12)
        num_keys = get_long_be(header, 0x38)

        read_keys = 0
        page = 1
        offset_vals = []
        database1 = []
        while read_keys < num_keys:
            file.seek(page_size * page)
            offsets = file.read((num_keys + 1) * 4 + 2)
            num_val = 0
            val = 1
            keys = 0
            i = 0
            while num_val != val:
                keys += 1
                key = get_short_le(offsets, 2 + i)
                val = get_short_le(offsets, 4 + i)
                num_val = get_short_le(offsets, 8 + i)
                offset_vals.append(key + page_size * page)
                offset_vals.append(val + page_size * page)
                read_keys += 1
                i += 4
            offset_vals.append(page_size * (page + 1))
            val_key = sorted(offset_vals)
            for i in range(keys * 2):
                file.seek(val_key[i])
                data = file.read(val_key[i + 1] - val_key[i])
                database1.append(data)
            page += 1

    database = {}
    for i in range(0, len(database1), 2):
        database[database1[i + 1]] = database1[i]
    return database


def decrypt_moz_3des(
        global_salt: bytes, master_password: bytes, entry_salt: bytes, encrypted_data: bytes
) -> bytes:
    hashed_password = sha1(global_salt + master_password).digest()
    pes = entry_salt + b"\x00" * (20 - len(entry_salt))
    chp = sha1(hashed_password + entry_salt).digest()
    k1_value = hmac.new(chp, pes + entry_salt, sha1).digest()
    tk_value = hmac.new(chp, pes, sha1).digest()
    k2_value = hmac.new(chp, tk_value + entry_salt, sha1).digest()
    k = k1_value + k2_value
    iv_value = k[-8:]
    key = k[:24]
    return DES3.new(key, DES3.MODE_CBC, iv_value).decrypt(encrypted_data)


def decode_login_data(data: str, key: bytes) -> str:
    asn1_data = decoder.decode(b64decode(data))
    iv_value = asn1_data[0][1][1].asOctets()
    ciphertext = asn1_data[0][2].asOctets()
    return unpad(DES3.new(key, DES3.MODE_CBC, iv_value).decrypt(ciphertext), 8).decode(
        "utf-8"
    )


def extract_secret_key(master_password: bytes, key_data: Dict[bytes, bytes]) -> bytes:
    cka_id = unhexlify("f8000000000000000000000000000001")
    password_check = key_data[b"password-check"]
    entry_salt_length = password_check[1]
    entry_salt = password_check[3: 3 + entry_salt_length]
    global_salt = key_data[b"global-salt"]

    priv_key_entry = key_data[cka_id]
    salt_length = priv_key_entry[1]
    name_length = priv_key_entry[2]

    priv_key_entry_asn1 = decoder.decode(
        priv_key_entry[3 + salt_length + name_length:]
    )
    entry_salt = priv_key_entry_asn1[0][0][1][0].asOctets()
    priv_key_data = priv_key_entry_asn1[0][1].asOctets()
    priv_key = decrypt_moz_3des(global_salt, master_password, entry_salt, priv_key_data)

    priv_key_asn1 = decoder.decode(priv_key)
    pr_key = priv_key_asn1[0][2].asOctets()

    pr_key_asn1 = decoder.decode(pr_key)
    key = long_to_bytes(pr_key_asn1[0][3])
    return key


def decrypt_pbe(decoded_item: Any, global_salt: bytes) -> bytes:
    entry_salt = decoded_item[0][0][1][0][1][0].asOctets()
    iteration_count = int(decoded_item[0][0][1][0][1][1])
    key_length = int(decoded_item[0][0][1][0][1][2])

    k = sha1(global_salt).digest()
    key = pbkdf2_hmac("sha256", k, entry_salt, iteration_count, dklen=key_length)

    iv_value = b"\x04\x0e" + decoded_item[0][0][1][1][1].asOctets()

    cipher_text = decoded_item[0][1].asOctets()
    clear_text = AES.new(key, AES.MODE_CBC, iv_value).decrypt(cipher_text)
    return clear_text


def get_firefox_key(directory: str) -> bytes:
    conn = sqlite3.connect(os.path.join(directory, "key4.db"))
    cursor = conn.cursor()

    cursor.execute("SELECT item1, item2 FROM metaData WHERE id = 'password';")
    row = cursor.fetchone()
    global_salt = row[0]
    item2 = row[1]

    decoded_item2 = decoder.decode(item2)
    clear_text = decrypt_pbe(decoded_item2, global_salt)
    cursor.execute("SELECT a11, a102 FROM nssPrivate;")
    row = cursor.fetchone()
    a11 = row[0]
    decoded_a11 = decoder.decode(a11)

    clear_text = decrypt_pbe(decoded_a11, global_salt)
    return clear_text[:24]
