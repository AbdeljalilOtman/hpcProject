# README

## Project Overview
This project consists of multiple components for resource monitoring, SLURM job scheduling, and a Dash application for visualization and management. Below are step-by-step instructions for setting up and running the project.

---

## Prerequisites
1. **Python Environment**:
   - Python version 3.8 or higher.
   - Install `virtualenv` if not already installed:
     ```bash
     pip install virtualenv
     ```
2. **SLURM Workload Manager**:
   - Ensure SLURM is installed and configured.
3. **Dependencies**:
   - Install dependencies listed in the `requirements.txt` file.

---

## Setting Up the Environment

### Step 1: Create a Virtual Environment
```bash
virtualenv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the SLURM Script

### Step 1: Verify SLURM Availability
Ensure that SLURM commands like `sinfo` and `squeue` are functional:
```bash
sinfo
```

### Step 2: Submit the SLURM Script
```bash
sbatch script.slurm
```

### Step 3: Monitor Job Status
```bash
squeue
```

---

## Running the Resource Monitoring Script

### Step 1: Make the Script Executable
```bash
chmod +x simlab.properties
```

### Step 2: Execute the Script
```bash
./simlab.properties
```
- **Customization**:
  - Modify environment variables before running the script:
    ```bash
    export PARTITION=gpu
    export MIN_CPUS=4
    export MIN_GPUS=1
    export REFRESH_INTERVAL=5
    ```

---

## Running the Python Scripts

### Running `connector.py`
1. Check if any specific configurations or arguments are required (refer to comments in the code).
2. Run the script:
   ```bash
   python connector.py
   ```

### Running `app.py`
1. Start the Dash application:
   ```bash
   python app.py
   ```
2. Open the application in a web browser at:
   ```
   http://127.0.0.1:8050
   ```

---

## Troubleshooting
1. **Dependency Issues**:
   - Ensure all dependencies are installed using the `requirements.txt` file.
2. **SLURM Errors**:
   - Check SLURM logs for errors after submitting a job.
3. **Debugging Python Scripts**:
   - Use verbose error logs by running the scripts with:
     ```bash
     python -m debugpy app.py
     ```

---

## Contact
For further assistance, please reach out to the project maintainer or refer to the comments in the source code.

