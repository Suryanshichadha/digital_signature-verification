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

footer_html ="""
    <style>
        .main {
            border: 5px solid #333;
            padding: 10px;
            border-radius: 10px;
        }
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f1f1f1;
            color: #333;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            border-top: 1px solid #ddd;
        }
    </style>
    <div class="footer">
        <p>© VIPS Digital Signature Application. All rights reserved </p>
        <p><a href="https://github.com/Suryanshichadha/digital_signature-verification" target="_blank">GitHub Repository</a></p>
    </div>"""

st.title("DOCUMENT AUTHENTICATION")
st.image("dig.png",width=400)


page = st.sidebar.selectbox("Choose a function", ["Home", "Sign Document", "Verify Document"])

st.sidebar.write("STEPS TO BE FOLLOWED")
st.sidebar.write("Select the function to be performed")
st.sidebar.write("1. If you want to generate sign for a document choose sign document from drop down and download the sign and hash")
st.sidebar.write("2. If you want to verify the document upload the documents and click verify ")

if page == "Home":
    st.write("WELCOME TO THE DOCUMENT AUTHENTICATION APPLICATION.")
    st.write("hello hope you are doing great and your documents too....")
    st.write("Let me help you with your document verification, i can also give a signature to your document.")
    st.write("This application helps you create a sign for your document and let you verify the integrity of the documents.")
    st.write("A digital signature is a mathematical scheme for verifying the authenticity and integrity of digital messages or documents.")
    st.write("Hash value is used to create a digital fingerprint of the document. Any change in the document, no matter how small, will produce a different hash value.")
elif page == "Sign Document":
    st.header("Sign Document")
    document = st.file_uploader("Upload Document to Sign", type=["txt", "pdf"])
    if document:
        doc_path = save_uploadedfile(document, "uploads")
        if st.button("Sign Document"):
            with st.spinner("Signing document..."):
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
            with st.spinner("Verifying document..."):
               is_valid = verify_document(doc_path, sig_path)
            if is_valid:
                st.success("Document is authentic and integrity is verified.")
            else:
                st.error("Document verification failed.")
st.markdown(footer_html, unsafe_allow_html=True)

