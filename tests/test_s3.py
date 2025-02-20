import os
import subprocess
from pathlib import Path
import boto3

def test_s3_upload():
    bucket_name = os.getenv("AWS_S3_BUCKET", "test-bucket")
    endpoint_url = os.getenv("AWS_S3_ENDPOINT", "http://127.0.0.1:9000")

    # Crear un archivo de prueba
    test_filename = "testfile.txt"
    with open(test_filename, "w") as f:
        f.write("Hello, MinIO!")

    # Subir el archivo al bucket
    result = subprocess.run(
        ["aws", "--endpoint-url", endpoint_url, "s3", "cp", test_filename, f"s3://{bucket_name}/"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Failed to upload file: {result.stderr}"

def test2_s3_upload():
    bucket_name = os.getenv("AWS_S3_BUCKET", "test-bucket")
    endpoint_url = os.getenv("AWS_S3_ENDPOINT", "http://127.0.0.1:9000")

    test_filename = "testfile.txt"
    with open(test_filename, "w") as f:
        f.write("Hello, MinIO!")

    s3root = f"s3://test-bucket/aaa"
    local_src = "assets/2.txt"
    # sync local source to s3
    filename = Path(local_src).name
    cmd = f"aws --endpoint-url http://127.0.0.1:9000 s3 cp {local_src} {s3root}/{filename}"
    print(f"copying source to s3: {cmd}")
    result = subprocess.run(cmd, shell=True, check=True)

    assert result.returncode == 0, f"Failed to upload file: {result.stderr}"

def test3_s3_upload():
    print("#####################")

    # Configuración de MinIO
    MINIO_URL = "http://127.0.0.1:9000"  # Reemplaza con la URL de tu MinIO
    ACCESS_KEY = "minioadmin"
    SECRET_KEY = "minioadmin"
    BUCKET_NAME = "test-bucket"  # Cambia esto por el nombre de tu bucket
    FILE_NAME = "archivo_prueba.txt"  # Archivo a crear y subir
    OBJECT_KEY = "archivo_prueba.txt"  # Nombre del archivo en MinIO

    # Crear cliente S3 para MinIO
    s3_client = boto3.client(
        "s3",
        endpoint_url=MINIO_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    print("Testear conexión listando buckets")
    response = s3_client.list_buckets()

    if "Buckets" in response:
        print("✅ Conexión exitosa a MinIO. Buckets disponibles:")
        for bucket in response["Buckets"]:
            print(f"- {bucket['Name']}")
    else:
        print("❌ Error: No se pudo obtener la lista de buckets.")

    print("Verificar si el bucket existe")
    response = s3_client.list_buckets()
    bucket_exists = any(bucket["Name"] == BUCKET_NAME for bucket in response["Buckets"])

    if bucket_exists:
        print(f"✅ Conexión exitosa: El bucket '{BUCKET_NAME}' existe en MinIO.")
    else:
        print(f"❌ Error: El bucket '{BUCKET_NAME}' no existe en MinIO.")

    print("1️⃣ Crear un archivo de prueba")
    with open(FILE_NAME, "w") as f:
        f.write("Este es un archivo de prueba para MinIO.")

    print("2️⃣ Subir el archivo con `aws s3 cp`")
    aws_s3_cp_command = [
        "aws", "s3", "cp",
        FILE_NAME,  # Archivo local
        f"s3://{BUCKET_NAME}/{OBJECT_KEY}",  # Destino en MinIO
        "--endpoint-url", MINIO_URL  # Indica que MinIO es el destino
    ]

    result = subprocess.run(aws_s3_cp_command, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ Archivo '{FILE_NAME}' subido correctamente a MinIO como '{OBJECT_KEY}'.")
    else:
        print(f"❌ Error al subir el archivo: {result.stderr}")

    print("3️⃣ Verificar si el archivo está en MinIO")
    objects = s3_client.list_objects_v2(Bucket=BUCKET_NAME)

    file_exists = any(obj["Key"] == OBJECT_KEY for obj in objects.get("Contents", []))

    if file_exists:
        print(f"✅ Archivo '{OBJECT_KEY}' verificado en MinIO.")
    else:
        print(f"❌ Error: El archivo '{OBJECT_KEY}' no está en MinIO.")

    print("4️⃣ Limpiar: eliminar el archivo local")
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)

    print("@@@@@@@@@@@@@@@@@@@")