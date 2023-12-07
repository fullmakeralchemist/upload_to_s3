import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd
import os

# Access Streamlit secrets
AWS_ACCESS_KEY_ID = st.secrets["aws_access_key_id"]
AWS_SECRET_ACCESS_KEY = st.secrets["aws_secret_access_key"]

# Replace 'your_bucket_name' with your actual S3 bucket name
DEFAULT_BUCKET_NAME = 'data-lake-traxion-pruebas'

# Function to upload a file to S3
def upload_to_s3(file_path, bucket_name, object_name):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-west-2')
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        return True
    except NoCredentialsError:
        st.error("Credenciales no disponibles")
        return False
    except Exception as e:
        st.error(f"Ocurrió un error: {str(e)}")
        return False

# Streamlit app
def main():
    st.title("Envio de Archivos CSV a S3")

    # File upload
    uploaded_file = st.file_uploader("Elige un Archivo CSV", type="csv")

    if uploaded_file is not None:
        # Display uploaded file
        st.success("Archivo subido de manera exitosa!")
        st.subheader("Archivo CSV subido:")
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        # S3 upload section
        st.subheader("Subir archivo a S3")

        # Use the default bucket name
        bucket_name = DEFAULT_BUCKET_NAME

        # Get custom file name from user input
        custom_file_name = "webtestst"

        # Use the custom file name in the object key
        if custom_file_name:
            object_name = f"st0-raw/streamlit/{custom_file_name}.csv"
        else:
            st.warning("Por favor, ingrese un nombre de archivo personalizado.")

        # Upload button
        if st.button("Sube archivo a S3") and custom_file_name:
            # Save the file locally
            local_file_path = "temp.csv"
            uploaded_file.seek(0)
            with open(local_file_path, "wb") as f:
                f.write(uploaded_file.read())

            # Upload the file to S3
            if upload_to_s3(local_file_path, bucket_name, object_name):
                st.success(f"Archivo subido exitosamente a un S3 bucket {bucket_name} con ruta y nombre {object_name}")
            else:
                st.error("Ha fallado la subida de archivo a S3. Revisa el mensaje de error de arriba.")
            
            # Cleanup: Remove the temporary local file
            st.text("Eliminando archivo...")
            try:
                os.remove(local_file_path)
            except Exception as e:
                st.warning(f"Failed to remove temporary file: {str(e)}")

if __name__ == "__main__":
    main()
