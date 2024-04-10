import argparse
import os
import requests

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input_dir", help="Path to the input directory")
args = parser.parse_args()

# Define template base URL
template_base_url = "https://github.com/wh/templates"

# Iterate through subdirectories in the input directory
for subdir in os.listdir(args.input_dir):
    # Check if subdir is a directory and contains input.properties
    if os.path.isdir(os.path.join(args.input_dir, subdir)) and os.path.exists(os.path.join(args.input_dir, subdir, "input.properties")):
        filepath = os.path.join(args.input_dir, subdir, "input.properties")

        # Read key-value pairs from the file
        with open(filepath, "r") as f:
            properties = dict(line.strip().split("=") for line in f if not line.startswith("#"))

        # Check for "force_run" input from manual trigger (optional)
        force_run = os.getenv("FORCE_RUN") == "true"  # Access environment variable

        # Get version, cluster, and namespace
        version = properties.get("VERSION")
        cluster = properties.get("TARGET-CLUSTER")
        namespace = properties.get("TARGET-NAMESPACE")

        # Only continue if there were input changes or a forced run
        if force_run or any(os.path.getmtime(os.path.join(args.input_dir, subdir, f)) > os.environ.get("GITHUB_SHA_TIME") for f in os.listdir(os.path.join(args.input_dir, subdir))):

            # Construct template URL with version as tag
            #template_url = f"{template_base_url}/archive/refs/tags/{version}.zip"

            # Download template zip file
            #response = requests.get(template_url, allow_redirects=True)
            #response.raise_for_status()

            # Create output directory using cluster and namespace
            output_dir = os.path.join('clusters', cluster, 'namespaces', namespace, 'cloud-infra')
            os.makedirs(output_dir, exist_ok=True)

            # Extract template zip to output directory (replace with your preferred tool)
            # Assuming you have unzip installed
            #os.system(f"unzip -q {response.content} -d {output_dir}")

            # Add and commit changes
            os.chdir(output_dir)  # Change directory to root of input dir for git commands
            os.system("git add .")
            os.system(f'git commit -m "Generated files for {cluster}/{namespace} ({version})"')
