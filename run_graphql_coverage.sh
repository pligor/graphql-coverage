#!/bin/bash

# Script Name: run_graphql_coverage.sh
# Description: Executes graphql_coverage.py for multiple GraphQL clients.
# Usage: ./run_graphql_coverage.sh

# Define an array of client names
clients=("InternalClient" "ExternalAuthClient" "ExternalPublicClient")

# Base directory for GraphQL clients
BASE_DIR="C:/Users/SFP7ZGX/Downloads/repos/Post.Taf.SendungenAPI/SendungenApi/GraphQlClients"

# Output directories
CSV_DIR="results/csv"
PNG_DIR="results/png"

# Create output directories if they do not exist
mkdir -p "$CSV_DIR"
mkdir -p "$PNG_DIR"

# Iterate over each client and execute the coverage script
for client in "${clients[@]}"; do
    echo "Processing client: $client"

    # Define paths for the current client
    SCHEMA_PATH="${BASE_DIR}/${client}/schema.graphql"
    QUERIES_PATH="${BASE_DIR}/${client}/Queries"
    CSV_PATH="${CSV_DIR}/${client}_schema_coverage_report.csv"
    PLOT_PATH="${PNG_DIR}/${client}_schema_coverage_chart.png"

    # Execute the GraphQL Coverage script
    python graphql_coverage.py \
        --schema_path "$SCHEMA_PATH" \
        --queries_path "$QUERIES_PATH" \
        --csv_path "$CSV_PATH" \
        --plot_path "$PLOT_PATH" \
		--only_leafs

    # Check if the script executed successfully
    if [ $? -eq 0 ]; then
        echo "Coverage analysis for $client completed successfully."
    else
        echo "Error: Coverage analysis for $client failed." >&2
    fi

    echo "---------------------------------------------"
done

echo "All coverage analyses completed."

