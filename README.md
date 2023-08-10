# vector_summarization

## Local Setup Instructions

1. Clone the repo anf Create a Python 3.10 virtual environmen:
   ```bash
   git clone https://github.com/alan-ai-learner/vector_summarization.git
   cd vector_summarization

   python3.10 -m venv venv
   source venv/bin/activate  # On Windows, use "venv\Scripts\activate"
   ```

2. Install the required dependencies using the provided requirements.txt file:
   ```
   pip install -r requirements.txt
   ```

3. Add your API key to the api.txt file:
   - Open the api_key.txt file in the root directory of the project.
   - Save the file.


## Run the Application

   ```
   uvicorn main:app --reload
   ```
   This will start the server at :
   ```
   http://localhost:8000/
   ```

## Docker setup:
1. Clone the repo  and change pwd to the cloned repo:
   ```bash
   git clone https://github.com/alan-ai-learner/vector_summarization.git
   cd vector_summarization
   ```
   
2. Build docker image:
   ```bash
   docker build -t langchain:latest path_to_dockerfile_directory
   ```
3. Run Docker image:
   ```bash
   
   docker run  -p 8000:8000 -v pdf/dir/path:/app/ langchain:latest
   
   ```
   Note:Let's say you have pdf files in /data directory then command will be.
   ```bash
   docker run -p 8000:8000 -v /data:/app/data langchain:latest
   ```
   This will start the server at :
   ```
   http://localhost:8000/
   ```
## How to use it:

## Endpoints

The API provides the following endpoints:
Note: Use the directory path used when runnning docker image (/data) , when using the below endpoint.
1. `/pdf_directory`
   List the contents of a PDF directory and generate vector embeddings.

   - **Method:** GET
   - **Endpoint:** `/pdf_directory`
   - **Parameters:** `directory_path` (string, required) - Path to the directory containing PDF files.
   - **Example usage:**

   ```bash
   curl --location --request GET 'http://localhost:8000/pdf_directory?directory_path=your/dir/path'
   ```

2.`/process_single_pdf`
   Process a single PDF file and generate its vector representation.

- **Method**: POST
- **Endpoint**: `/process_single_pdf`
- **Parameters**: `f (`file, required) - PDF file to be processed.
- **Example usage**:
```bash
curl --location --request POST 'http://localhost:8000/process_single_pdf' \
--form 'f=@"/pat/to/pdf/file"'
```

3. `/query`

   Query the vector representations for an answer to a given question.

- **Method:** POST
- **Endpoint:** `/query`
- **Parameters:** JSON payload containing `query` (string) and `filename` (string) representing the question and the filename of the processed PDF.
- **Example usage:**

```bash
curl --location --request POST 'http://localhost:8000/query' \
--header 'Content-Type: application/json' \
--data-raw '{
    "query": "your query",
    "filename": "you pdf file name with extension, exp :test.pdf"
}'
```

4. `/summarizer`

Generate a summary of the content in a PDF file.

- **Method:** POST
- **Endpoint:** `/summarizer`
- **Parameters:** `input_summary_file` (file, required) - PDF file for which the summary is to be generated.
- **Example usage:**

```bash
curl --location --request POST 'http://localhost:8000/summarizer' \
--form 'input_summary_file=@"path/to/pdf/file"'
```
