# zepto-data-ai-platform



\# Zepto Data \& AI Platform



This project contains three modules:



1\. Data Pipeline

2\. Analytics

3\. Support Assistant



Each module is kept inside its own folder and can be run separately.



\## Project Structure



```text

zepto-data-ai-platform/

│

├── data\_pipeline/

│   ├── data\_pipeline.ipynb

│   └── zepto\_books.db

│

├── analytics/

│   ├── analytics\_01\_eda.ipynb

│   ├── analytics\_02\_modeling.ipynb

│   ├── titanic.csv

│   ├── best\_pipeline.joblib

│   └── README.md

│

├── support\_assistant/

│   ├── docs/

│   ├── main.py

│   ├── Dockerfile

│   ├── requirements.txt

│   └── README.md

│

└── requirements.txt

```



\## Installation



Install the project requirements from the repository root:



```bash

pip install -r requirements.txt

```



\# Module 1 - Data Pipeline



The data pipeline module contains the scraping, cleaning and SQLite database work.



Open:



```text

data\_pipeline/data\_pipeline.ipynb

```



Run the notebook cells in order.



The SQLite database created by the module is saved as:



```text

data\_pipeline/zepto\_books.db

```



\# Module 2 - Analytics



The analytics module contains the Titanic EDA and modeling work.



Move to the analytics folder or open the notebooks from that folder.



Run the notebooks in this order:



```text

analytics\_01\_eda.ipynb

analytics\_02\_modeling.ipynb

```



`titanic.csv` is included inside the analytics folder as the offline dataset used by the modeling notebook.



The saved final model pipeline is also included in the analytics folder.



More details and written interpretations are available in:



```text

analytics/README.md

```



\# Module 3 - Support Assistant



The support assistant is a RAG based FastAPI application using the 8 Zepto policy documents.



Move to the module folder:



```bash

cd support\_assistant

```



Install the module requirements:



```bash

pip install -r requirements.txt

```



Start the API:



```bash

uvicorn main:app --reload

```



Open:



```text

http://127.0.0.1:8000/docs

```



Use the `POST /ask` endpoint to test the assistant.



The application runs with `MOCK\_LLM=1` by default, so no LLM API key is required.



Docker can also be used from the project root:



```bash

docker build -f support\_assistant/Dockerfile -t zepto-support .

docker run -p 7860:7860 zepto-support

```



Then open:



```text

http://127.0.0.1:7860/docs

```



More details about the RAG architecture and example API responses are available in:



```text

support\_assistant/README.md

```

