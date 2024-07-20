import streamlit as st
from sign_document import sign_document
from verify_document import verify_document
import os

def save_uploadedfile(uploadedfile, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, uploadedfile.name)
    with open(file_path, "wb") as f:
        f.write(uploadedfile.read())
    return file_path

st.title("Digital Signature Application")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a function", ["Home", "Sign Document", "Verify Document"])

if page == "Home":
    st.write("Welcome to the Digital Signature Application.")

elif page == "Sign Document":
    st.header("Sign Document")
    document = st.file_uploader("Upload Document to Sign", type=["txt", "pdf"])
    if document:
        doc_path = save_uploadedfile(document, "uploads")
        if st.button("Sign Document"):
            signature_path, hash_path = sign_document(doc_path)
            st.success(f"Document signed successfully.\nSignature saved to {signature_path}\nHash saved to {hash_path}")
            st.download_button(label="Download Signature", data=open(signature_path, "rb").read(), file_name=os.path.basename(signature_path))
            st.download_button(label="Download Hash", data=open(hash_path, "rb").read(), file_name=os.path.basename(hash_path))

elif page == "Verify Document":
    st.header("Verify Document")
    document = st.file_uploader("Upload Document", type=["txt", "pdf"])
    signature = st.file_uploader("Upload Signature", type=["sig"])
    if document and signature:
        doc_path = save_uploadedfile(document, "uploads")
        sig_path = save_uploadedfile(signature, "uploads")
        if st.button("Verify Document"):
            is_valid = verify_document(doc_path, sig_path)
            if is_valid:
                st.success("Document is authentic and integrity is verified.")
            else:
                st.error("Document verification failed.")
