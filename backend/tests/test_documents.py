import pymupdf


def test_upload_valid_pdf(client):
    with pymupdf.open() as pdf:
        pdf.new_page()
        pdf.new_page()
        pdf_data = pdf.tobytes()

    response = client.post("/api/documents", files={"file": ("test.pdf", pdf_data)})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test.pdf"
    assert data["status"] == "processing"
    assert "file_path" not in data


def test_upload_reject_non_pdf(client):
    response = client.post("/api/documents", files={"file": ("test.pdf", b"not a pdf")})
    assert response.status_code == 415


def test_list_documents(client):
    response = client.get("/api/documents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
