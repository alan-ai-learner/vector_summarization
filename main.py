from fastapi import FastAPI, Request, Response, UploadFile, File
from pydantic import BaseModel
import uvicorn
from langchain_info import LangChainApp  # Import the LangChainApp class
from logger_config import logger
from fastapi.responses import JSONResponse
import os
import tempfile

app = FastAPI()
app_instance = LangChainApp()  # Create an instance of LangChainApp

ALLOWED_ORIGINS = "*"

# Handle CORS preflight requests
@app.options('/{rest_of_path:path}')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response

# Set CORS headers
@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response

class QueryInfo(BaseModel):
    query: str
    filename: str

@app.get("/pdf_directory")
async def list_directory(directory_path: str):
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return JSONResponse(content={"error": "Invalid directory path"}, status_code=400)
    else:
        app_instance.pdf_dir_to_vectors(directory_path)  # Use the app instance
        return {"message": "Embeddings have been generated for the directory. You can query them using the 'query' endpoint."}

@app.post("/process_single_pdf")
async def process_single_pdf(f: UploadFile = File(...)):
    try:
        if f.content_type != "application/pdf":
            return JSONResponse(content={"error": "Invalid file type. Only PDF files are allowed."}, status_code=400)

        f_name = f.filename
        logger.info("Processing file: %s", f_name)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(f.file.read())
            temp_pdf_path = temp_pdf.name

        app_instance.pdf_to_vectors(temp_pdf_path, f_name)  # Use the app instance

        return {"message": "Vector generated successfully. You can now query them on the 'query' endpoint."}
    except Exception as e:
        logger.error("Error processing PDF: %s", str(e))
        return JSONResponse(content={"error": "An error occurred while processing the PDF."}, status_code=500)

@app.post("/query")
async def query_vectors(query_info: QueryInfo):
    try:
        question = query_info.query
        filename = query_info.filename
        logger.info("Querying: %s from %s", question, filename)
        retriever = app_instance.query(filename)  # Use the app instance
        answer = retriever({"query": question})
        return {"answer": answer}
    except Exception as e:
        logger.error("Error querying vectors: %s", str(e))
        return JSONResponse(content={"error": "An error occurred while querying vectors."}, status_code=500)

@app.post("/summarizer")
async def summarizer_endpoint(input_summary_file: UploadFile = File(...)):
    try:
        if input_summary_file.content_type != "application/pdf":
            return JSONResponse(content={"error": "Invalid file type. Only PDF files are allowed."}, status_code=400)

        logger.info("Processing input file: %s", input_summary_file.filename)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(input_summary_file.file.read())
            temp_input_summary_file = temp_pdf.name

        logger.info("Generating summaries...")
        summary = app_instance.summarizer(temp_input_summary_file)  # Use the app instance

        return {"summary": summary}
    except Exception as e:
        logger.error("Error generating summary: %s", str(e))
        return JSONResponse(content={"error": "An error occurred while generating the summary."}, status_code=500)

if __name__ == "__main__":
    logger.info("Starting the server...")
    host = "127.0.0.1" 
    port = 8000
    uvicorn.run(app, host=host, port=port)
