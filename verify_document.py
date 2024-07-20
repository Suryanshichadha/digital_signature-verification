import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

def verify_document(document_path, signature_path):
    with open(document_path, 'rb') as doc_file:
        document = doc_file.read()

    document_hash = hashlib.sha256(document).digest()

    with open(signature_path, 'rb') as sig_file:
        signature = sig_file.read()

    with open("public_key.pem", "rb") as key_file:
        public_key = load_pem_public_key(key_file.read())

    try:
        public_key.verify(
            signature,
            document_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False
