import logging
from enum import Enum
from typing import List, Tuple

from config.logger_config import setup_logging

setup_logging()


class Key(Enum):
    P = 23
    Q = 97
    E = 101


def mod_inv(a_value: int, m_value: int) -> int:
    logging.info("Performing modular inverse calculation...")
    g_value, x_value, _ = egcd(a_value, m_value)
    if g_value != 1:
        raise ValueError
    logging.info("Modular inverse calculation successful.")
    return x_value % m_value


def gcd(a_value: int, b_value: int) -> int:
    logging.info("Calculating Greatest Common Divisor...")
    while b_value != 0:
        a_value, b_value = b_value, a_value % b_value
    return a_value


def egcd(a_value: int, b_value: int) -> Tuple[int, int, int]:
    logging.info("Extended Euclidean Algorithm running...")
    if a_value == 0:
        return (b_value, 0, 1)
    g_value, y_value, x_value = egcd(b_value % a_value, a_value)
    return (g_value, x_value - (b_value // a_value) * y_value, y_value)


def encrypt(plaintext: str, public_key: Tuple[int, int]) -> List[int]:
    logging.info("Encrypting plaintext...")
    e_value, n_value = public_key
    ciphertext = [(ord(char) ** e_value) % n_value for char in plaintext]
    return ciphertext


def decrypt(ciphertext: List[int], private_key: Tuple[int, int]) -> str:
    logging.info("Decrypting ciphertext...")
    d_value, n_value = private_key
    plaintext = [chr((char**d_value) % n_value) for char in ciphertext]
    return "".join(plaintext)


def generate_keypair(
    p_value: int, q_value: int, e_value: int
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    logging.info("Generating keypair...")
    n_value = p_value * q_value
    phi = (p_value - 1) * (q_value - 1)
    d_value = mod_inv(e_value, phi)
    return (e_value, n_value), (d_value, n_value)


def encrypt_file(
    input_file: str, output_file: str, public_key: Tuple[int, int]
) -> None:
    logging.info("Starting file encryption...")
    with open(input_file, "r", encoding="utf-8") as f_in, open(
        output_file, "w", encoding="utf-8"
    ) as f_out:
        plaintext = f_in.read()
        ciphertext = encrypt(plaintext, public_key)
        f_out.write(",".join(str(char) for char in ciphertext))
    logging.info("File encryption successful.")


def decrypt_file(
    input_file: str, output_file: str, private_key: Tuple[int, int]
) -> None:
    logging.info("Starting file decryption...")
    with open(input_file, "r", encoding="utf-8") as f_in, open(
        output_file, "w", encoding="utf-8"
    ) as f_out:
        ciphertext = f_in.read().split(",")
        cipherint = [int(char) for char in ciphertext]
        plaintext = decrypt(cipherint, private_key)
        f_out.write(plaintext)
    logging.info("File decryption successful.")


input_file_dir: str = "data/input.txt"
output_file_dir: str = "data/output.txt"
p: int = Key.P.value
q: int = Key.Q.value
e: int = Key.E.value
gen_public_key, gen_private_key = generate_keypair(p, q, e)

encrypt_file(input_file_dir, "data/encrypted.txt", gen_public_key)

decrypt_file("data/encrypted.txt", output_file_dir, gen_private_key)


with open(output_file_dir, "r", encoding="utf-8") as f:
    decrypted_text: str = f.read()
print("Decrypted text:", decrypted_text)

logging.info("Encryption and decryption process complete.")
