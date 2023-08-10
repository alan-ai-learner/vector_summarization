import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain import OpenAI, PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chains.summarize import load_summarize_chain
from logger_config import logger

class LangChainApp:
    def __init__(self):
        self.api_key = self.read_api_key_from_file("api_key.txt")
        os.environ["OPENAI_API_KEY"] = self.api_key
        self.embeddings = OpenAIEmbeddings()


    def read_api_key_from_file(self, file_path):
        logger.info("Reading API key from file")
        try:
            with open(file_path, 'r') as file:
                api_key = file.read().strip()  # Read the key from the file and remove leading/trailing whitespaces
            return api_key
        except FileNotFoundError:
            logger.error(f"Error: The file '{file_path}' was not found.")
            return None

    def pdf_dir_to_vectors(self, pdf_directory):
        logger.info("Inside pdf to vectors directory")
        logger.info(f"Fetching... {pdf_directory}")
        index_file = f"{pdf_directory}.index"
        if not os.path.exists(index_file):
            logger.info("Generating PDF directory vectors")
            loader = DirectoryLoader(pdf_directory, loader_cls=TextLoader,glob='**/*.pdf')
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.split_documents(documents)
            docsearch = FAISS.from_documents(texts, self.embeddings)
            docsearch.save_local(index_file)
            logger.info("Successfully generated embedded documents for directory: {}".format(pdf_directory))
        else:
            logger.info("Embedded documents are already present. Please query using the query endpoint.")

    def pdf_to_vectors(self, f, f_name):
        logger.info("Inside pdf_to_vectors")
        loader = PyPDFLoader(f)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        docsearch = FAISS.from_documents(texts, self.embeddings)
        docsearch.save_local(f"{f_name}.index")

    def summarizer(self, f_name):
        logger.info("Inside summary generator")
        loader = PyPDFLoader(f_name)
        pages = loader.load()
        text = "\n".join(page.page_content for page in pages)
        text = text.replace('\t', ' ')
        text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)
        docs = text_splitter.create_documents([text])
        map_prompt = """
                    Write a concise summary of the following:
                    "{text}"
                    CONCISE SUMMARY:
                    """
        map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])
        combine_prompt = """
                            Write a concise summary of the following text delimited by triple backquotes.
                            Return your response in bullet points which cover the key points of the text.
                            ```{text}```
                            BULLET POINT SUMMARY:
                            """
        combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])
        summary_chain = load_summarize_chain(llm=OpenAI(),
                                             chain_type='map_reduce',
                                             map_prompt=map_prompt_template,
                                             combine_prompt=combine_prompt_template,
                                            )
        output = summary_chain.run(docs)
        return output

    def query(self, f_name):
        try:
            emb_loader = FAISS.load_local(f"{f_name}.index", self.embeddings)
            retriever = emb_loader.as_retriever()
            qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True)
            return qa
        except Exception as e:
            logger.error("Error querying vectors: %s", str(e))
            return None

