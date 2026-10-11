# Run the MVP on Windows

Use 64-bit Python 3.12. Check it in PowerShell:

```powershell
py -3.12 --version
```

If Python 3.12 is missing, install it from the
[official Python 3.12.10 Windows download page](https://www.python.org/downloads/release/python-31210/).
Choose **Windows installer (64-bit)**, include the Python launcher, and reopen
PowerShell after installation.

Extract the entire `OPG-Streamlit-MVP.zip` archive. Open the extracted
`OPG-Streamlit-MVP` folder containing `requirements-app.txt`, `app`, `models`,
`analysis`, and `tools`. Right-click inside the folder and select **Open in
Terminal**, or open PowerShell in that folder from File Explorer.

Run these commands once:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-app.txt
```

Start the app:

```powershell
.\.venv\Scripts\python.exe tools\run_app.py
```

Open **http://localhost:8501** in your browser. This address reaches the app
running on your own computer. Leave the terminal open while using the app.

For the first demonstration, click **Use synthetic example**, then **Run
analysis**. The sidebar provides eligibility/receipt results, model predictions,
and report exports. Stop the app with **Ctrl+C** in the terminal.

On later visits, open PowerShell in the same folder and run only the start
command. Virtual-environment activation and PowerShell execution-policy changes
are unnecessary because these commands call its Python executable directly.

The ZIP includes the frozen model and required scientific source modules. Git
and the historical survey datasets are not needed for a synthetic demonstration.
Keep the extracted files together and preserve the scientific source files,
because the model checks their integrity. For your own CSV, use the app's
synthetic template and [data dictionary](data_dictionary.md).

If port 8501 is already in use, stop the other local app or choose another port:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app\Home.py --server.address 127.0.0.1 --server.port 8502 --browser.gatherUsageStats false
```

Then open `http://localhost:8502`. If any setup command fails, retain its exact
terminal output so the failure can be diagnosed.
