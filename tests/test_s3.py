import os
import subprocess
from pathlib import Path

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
