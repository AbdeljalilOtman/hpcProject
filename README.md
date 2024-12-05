
# Simlab Resource Manager

This is a Dash-based web application that allows users to manage and view the available resources (CPUs and GPUs) across different partitions in a cluster. It provides a user-friendly interface to select a partition and retrieve real-time information about the resources available for that partition.

## Features

- **Partition Selection**: Users can select from various predefined partitions (`defq`, `gpu`, `shortq`, `longq`, `visu`, `special`).
- **Resource Availability**: For each selected partition, the app displays the available CPUs and GPUs.
- **Modular Architecture**: The app is divided into frontend and backend components for better maintainability and scalability.

## Project Structure

```
your_project/
├── app.py                    # Main entry point for the Dash app
├── frontend/                 # UI-related files
│   ├── __init__.py           # Initialize frontend package
│   ├── app_layout.py         # Layout components for the Dash app
│   ├── assets/               # CSS and static files
│   │   └── styles.css        # Custom CSS for styling the UI
├── backend/                  # Logic and data handling
│   ├── __init__.py           # Initialize backend package
│   ├── connector.py          # Logic to retrieve resource data
│   ├── credentials_manager.py# Handles credentials management for data retrieval
└── scripts/                  # Shell scripts and other automation
    ├── script.sh             # Script for retrieving availabe resources
```




## Setup Instructions

To run the project, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install the required dependencies**:

   The project requires Python and the `dash` library. You can install the dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not present, you can install Dash manually:

   ```bash
   pip install dash
   ```

3. **Create a `credentials.properties` file**:

   You need to create a `credentials.properties` file where you will store your Simlab credentials. This file should include the following:

   ```
   simlab.username=<your-username>
   simlab.password=<your-password>
   ```

   Make sure the file is saved securely and not exposed to unauthorized access.

4. **Create the `proj.sh` file**:

   In your simlab account, create a directory called `project` and inside it , create the `proj.sh` file. Copy the contents of `Scripts/script.sh` into this new file. 

5. **Run the application**:

   To start the app, run the following command:

   ```bash
   python app.py
   ```

   The app will start a local development server, and you can access it in your browser at `http://127.0.0.1:8050`.

## How It Works

1. **Frontend**: 
   - The layout and UI components are defined in `frontend/app_layout.py`. The UI consists of a dropdown to select a partition and sections to display CPU and GPU resource availability.
   - The `styles.css` file in the `frontend/assets` folder is used for styling the app.

2. **Backend**: 
   - The `connector.py` file in the `backend` folder contains the logic for retrieving resource data. Currently, it simulates resource data for each partition.
   - The `credentials_manager.py` file is responsible for managing sensitive credentials required for data retrieval, ensuring secure access to resources.

3. **Callbacks**: 
   - The Dash app uses callbacks to update the UI based on user input. When the user selects a partition from the dropdown, the app fetches and displays the corresponding CPU and GPU availability.

4. **Scripts**:
   - The `scripts/script.sh` file  containes the mechanism to retrieve available resources from a given partition using `sinfo`.






