from dash import Dash, Input, Output, dcc, html
from frontend import get_layout  # Import the layout from the frontend module
from backend import Connector  # Import the backend connector

class DashApp:
    def __init__(self, app):
        self.app = app
        self.connector = Connector()
        self.partitions = ['defq', 'gpu', 'shortq', 'longq', 'visu', 'special']
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        """Define the layout of the Dash app."""
        # Layout with loading component around outputs
        self.app.layout = get_layout(self.partitions)

    def setup_callbacks(self):
        """Set up the callbacks to update the UI based on user input."""
        @self.app.callback(
            [Output("cpu-output", "children"),
             Output("gpu-output", "children")],
            [Input("partition-dropdown", "value")]
        )
        def update_resources(selected_partition):
            if not selected_partition:
                return "Available CPUs: -", "Available GPUs: -"

            # Fetch resource details for the selected partition
            partition_data = self.connector.get_resources(selected_partition)
            if partition_data:
                return (
                    f"Available CPUs: {partition_data[0]}",
                    f"Available GPUs: {partition_data[1]}"
                )
            else:
                return "Failed to retrieve CPUs", "Failed to retrieve GPUs"

# Create Dash app and run
if __name__ == "__main__":
    app = Dash(__name__)
    DashApp(app)  # Initialize the DashApp
    app.run_server(debug=True)
