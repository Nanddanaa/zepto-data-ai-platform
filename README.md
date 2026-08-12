## Installation and Setup

### 1. Clone the Repository

Open Command Prompt and move to the folder where you want to download the project. For example:

```bat
cd C:\Users\<username>\Downloads
```

Clone the repository:

```bat
git clone <repository-url>
```

Move into the project:

```bat
cd zepto-data-ai-platform
```

### 2. Create a Python Virtual Environment

All of this must be done in **Command Prompt (CMD)** inside your project folder.

First, open CMD and go to the project directory:

```bat
cd C:\Users\<username>\Downloads\zepto-data-ai-platform
```

Then create the virtual environment:

```bat
python -m venv .venv
```

Activate it on Windows:

```bat
.venv\Scripts\activate
```

After activation, your terminal will show `(.venv)` at the beginning.

Example:

```text
(.venv) C:\Users\<username>\Downloads\zepto-data-ai-platform>
```

### 3. Install the Requirements

Install all project dependencies:

```bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Wait until the installation is complete before opening the notebooks.

### 4. Open the Project in VS Code

From the same command prompt, run:

```bat
code .
```

If the `code` command is not available, open VS Code manually and select **File → Open Folder**, then open the `zepto-data-ai-platform` folder.

### 5. Select the Notebook Kernel

When a `.ipynb` notebook is opened in VS Code:

1. Click **Select Kernel** at the top-right.
2. Select **Python Environments**.
3. Select the `.venv` environment created above.
4. Click **Run All** to execute the notebook.

The same `.venv` can be used for all modules.

---

## Module 1 - Data Pipeline

Open:

```text
data_pipeline/data_pipeline.ipynb
```

Select `.venv` as the kernel and click **Run All**.

The notebook performs the data pipeline and creates the SQLite database used in the module.

---

## Module 2 - Analytics

Run the analytics notebooks in this order:

```text
1. analytics/analytics_01_eda.ipynb
2. analytics/analytics_02_modeling.ipynb
```

### EDA Notebook

First open:

```text
analytics/analytics_01_eda.ipynb
```

Select `.venv` and click **Run All**.

The notebook loads the Titanic dataset and saves it as:

```text
titanic.csv
```

### Modeling Notebook

After the EDA notebook has completed, open:

```text
analytics/analytics_02_modeling.ipynb
```

Select the same `.venv` kernel and click **Run All**.

This notebook reads `titanic.csv` and performs preprocessing, model training and evaluation.

---

## Module 3 - Support Assistant

Open a terminal from the repository root and make sure `.venv` is activated.

Move to the support assistant folder:

```bat
cd support_assistant
```

Start the FastAPI application:

```bat
uvicorn main:app --reload
```

After the server starts, open:

```text
http://127.0.0.1:8000/docs
```

Use the `POST /ask` endpoint to test the application.

Press `Ctrl+C` in the terminal to stop the server.

### Docker

Docker can also be used from the repository root.

If currently inside `support_assistant`, return to the root:

```bat
cd ..
```

Build the image:

```bat
docker build -f support_assistant/Dockerfile -t zepto-support .
```

Run the container:

```bat
docker run -p 7860:7860 zepto-support
```

Then open:

```text
http://127.0.0.1:7860/docs
```
