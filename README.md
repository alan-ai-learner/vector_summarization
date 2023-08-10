# vector_summarization

## Setup Instructions

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


```