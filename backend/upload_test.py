import base64
import json
import urllib.request
from pathlib import Path

def test_upload():
    url = "http://localhost:8000/graphql"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MDliNjQwYi04YzY4LTQ2YzgtOGVhZC1hZWFlZmFhMGMwYzUiLCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInJvbGUiOiJVU0VSIiwiaWF0IjoxNzc3NDgyNzY1LCJleHAiOjE3Nzc1NjkxNjV9.F_-6wzjDFUtprFBFSsg5BPFLSn6tjF7pjU5F7bcUFEo"

    image_path = Path(r"C:\Users\hufer\Desktop\personal symfony\Proyecto-ia-dental\entrenamiento ia pruebas\Ortopantomografia.002.jpg")

    print(f"Leyendo imagen: {image_path.name} ({image_path.stat().st_size} bytes)")
    file_base64 = base64.b64encode(image_path.read_bytes()).decode()

    query = """
    mutation UploadFile($fileBase64: String!, $fileName: String!, $mimeType: String!) {
        uploadRadiography(fileBase64: $fileBase64, fileName: $fileName, mimeType: $mimeType) {
            success
            message
            analysis {
                analysisId
                status
            }
        }
    }
    """

    payload = json.dumps({
        "query": query,
        "variables": {
            "fileBase64": file_base64,
            "fileName": image_path.name,
            "mimeType": "image/jpeg"
        }
    }).encode()

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
        print(json.dumps(result, indent=2))

test_upload()