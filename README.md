# Zepto Data & AI Platform

This repository contains three modules:

1. **Data Pipeline** – web scraping, data cleaning and SQLite storage
2. **Analytics** – Titanic exploratory data analysis and machine learning
3. **Support Assistant** – RAG-based Zepto policy assistant using FastAPI

Each module is kept in its own folder and can be executed separately.

## Project Structure

```text
zepto-data-ai-platform/
│
├── data_pipeline/
│   ├── data_pipeline.ipynb
│   └── zepto_books.db
│
├── analytics/
│   ├── analytics_01_eda.ipynb
│   ├── analytics_02_modeling.ipynb
│   ├── titanic.csv
│   ├── best_pipeline.joblib
│   └── README.md
│
├── support_assistant/
│   ├── docs/
│   ├── main.py
│   ├── Dockerfile
│   └── README.md
│
├── requirements.txt
└── README.md
```

# Setup

## 1. Clone the Repository

Open Command Prompt or a terminal in the folder where you want to download the project.

```bash
git clone <repository-url>
cd zepto-data-ai-platform
```

## 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bat
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

After activation, the terminal should show `(.venv)`.

## 3. Install Requirements

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install all project dependencies:

```bash
pip install -r requirements.txt
```

The root `requirements.txt` contains the dependencies required for all three modules, so the installation only needs to be done once.

## 4. Open the Project in VS Code

Open the repository in VS Code:

```bash
code .
```

If the `code` command is unavailable, open VS Code manually and select:

**File → Open Folder → zepto-data-ai-platform**

## 5. Select the Notebook Kernel

For the `.ipynb` notebooks:

1. Open the notebook in VS Code.
2. Click **Select Kernel** at the top-right.
3. Select **Python Environments**.
4. Select the `.venv` environment created during setup.
5. Click **Run All**.

The same `.venv` environment can be used for all modules.

---

# Module 1 – Data Pipeline

Open:

```text
data_pipeline/data_pipeline.ipynb
```

Click **Run All**.

The notebook performs web scraping, data cleaning and transformation, and stores the processed data in SQLite.

The resulting database is:

```text
data_pipeline/zepto_books.db
```

---

# Module 2 – Analytics

Run the analytics notebooks in this order:

```text
1. analytics/analytics_01_eda.ipynb
2. analytics/analytics_02_modeling.ipynb
```

## Step 1 – Exploratory Data Analysis

Open:

```text
analytics/analytics_01_eda.ipynb
```

Click **Run All**.

The notebook loads the Titanic dataset using Seaborn and performs exploratory data analysis.

It saves the dataset as:

```text
analytics/titanic.csv
```

`titanic.csv` is also included in the repository so the dataset is available with the project.

## Step 2 – Modeling

After the EDA notebook has completed, open:

```text
analytics/analytics_02_modeling.ipynb
```

Click **Run All**.

The modeling notebook reads `titanic.csv` and performs preprocessing, model training, evaluation and model selection.

The final trained pipeline is saved as:

```text
analytics/best_pipeline.joblib
```

Detailed analysis and interpretations are available in:

```text
analytics/README.md
```

---

# Module 3 – Support Assistant

The Support Assistant is a RAG-based FastAPI application that answers questions using the 8 provided Zepto policy documents.

VS Code is not required to run this module.

Open a terminal from the repository root. If the virtual environment is not currently active, activate it on Windows using:

```bat
.venv\Scripts\activate
```

Move to the module folder:

```bash
cd support_assistant
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

When the server starts, open:

```text
http://127.0.0.1:8000/docs
```

Use the **POST `/ask`** endpoint and click **Try it out**.

Example request:

```json
{
  "query": "What is the delivery fee?"
}
```

Click **Execute** to view the response.

The application uses `MOCK_LLM=1` by default, so an external LLM API key is not required for the default execution.

Press `Ctrl+C` in the terminal to stop the server.

More details about the RAG architecture and example responses are available in:

```text
support_assistant/README.md
```

---

# Docker – Support Assistant

The Support Assistant can optionally be run using Docker. I have created requirements in support_assistant because docker using that requirements only because main requirements many things that not needed.

Make sure Docker Desktop is installed and running.

Run the following command from the **repository root**:

```bash
docker build -f support_assistant/Dockerfile -t zepto-support .
```

After the image is built successfully, run:

```bash
docker run -p 7860:7860 zepto-support
```

Then open:

```text
http://127.0.0.1:7860/docs
```

Use the same **POST `/ask`** endpoint to test the containerized application.
