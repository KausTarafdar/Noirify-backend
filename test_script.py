import os
import httpx

BASE_URL = "http://localhost:8000/process"  # Replace with your FastAPI server's base URL
UPLOAD_ENDPOINT = f"{BASE_URL}/upload/"  # Endpoint for uploading chunks
TEST_FILE_PATH = "/home/kaytee/test_file.mkv"  # Replace with the path to your test file
CHUNK_SIZE = 1024 * 1024  # 1 MB chunks

def split_file_into_chunks(file_path, chunk_size):
    """Generator to split a file into chunks."""
    with open(file_path, "rb") as file:
        while chunk := file.read(chunk_size):
            yield chunk

def test_chunked_upload():
    """Test the chunked file upload process."""
    if not os.path.exists(TEST_FILE_PATH):
        print(f"Test file not found: {TEST_FILE_PATH}")
        return

    file_name = os.path.basename(TEST_FILE_PATH)
    file_size = os.path.getsize(TEST_FILE_PATH)
    total_chunks = (file_size + CHUNK_SIZE - 1) // CHUNK_SIZE  # Calculate total chunks

    print(f"Starting upload: {TEST_FILE_PATH}")
    print(f"File size: {file_size} bytes, Total chunks: {total_chunks}")

    # Split and upload chunks
    for chunk_number, chunk in enumerate(split_file_into_chunks(TEST_FILE_PATH, CHUNK_SIZE), start=1):
        # Create multipart FormData
        files = {
            "file_chunk": (f"chunk_{chunk_number}", chunk, "application/octet-stream")
        }
        data = {
            "chunk_number": str(chunk_number),
            "total_chunks": str(total_chunks)
        }

        # Send the chunk as FormData
        try:
            response = httpx.post(UPLOAD_ENDPOINT, files=files, data=data)
            response.raise_for_status()  # Raise exception for HTTP errors
        except httpx.RequestError as exc:
            print(f"An error occurred while uploading chunk {chunk_number}: {exc}")
            return
        except httpx.HTTPStatusError as exc:
            print(f"Server returned an error: {exc.response.text}")
            return

        # Process response
        resp_data = response.json()
        if chunk_number == total_chunks:
            print(f"Upload complete. Server response: {resp_data}")
        else:
            print(f"Chunk {chunk_number}/{total_chunks} uploaded successfully.")


if __name__ == "__main__":
    test_chunked_upload()
