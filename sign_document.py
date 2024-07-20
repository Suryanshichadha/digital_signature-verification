import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key

def sign_document(document_path):
    with open(document_path, 'rb') as doc_file:
        document = doc_file.read()

    document_hash = hashlib.sha256(document).digest()

    with open("private_key.pem", "rb") as key_file:
        private_key = load_pem_private_key(key_file.read(), password=None)

    signature = private_key.sign(
        document_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    sig_file_path = document_path + ".sig"
    hash_file_path = document_path + ".hash"

    with open(sig_file_path, 'wb') as sig_file:
        sig_file.write(signature)
    with open(hash_file_path, 'wb') as hash_file:
        hash_file.write(document_hash)

    return sig_file_path, hash_file_path
