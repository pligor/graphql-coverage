# GraphQL Coverage

## Overview

GraphQL Coverage is a powerful tool designed to assess how extensively your GraphQL schema is utilized by your queries. By analyzing the fields defined in your schema and comparing them against the fields used in your queries, this tool provides valuable insights into the coverage and potential gaps within your GraphQL implementation.

While the Jupyter Notebook (`graphql_coverage.ipynb`) serves as a playground for exploratory analysis, the primary interface for users is the command-line script (`graphql_coverage.py`). This README will guide you through the installation, usage, and functionalities of the CLI tool.

## Features

- **Comprehensive Field Extraction**: Extracts all fields or only leaf fields from your GraphQL schema.
- **Query Analysis**: Parses and analyzes GraphQL queries to determine field usage.
- **Coverage Calculation**: Computes the percentage of schema fields utilized by queries.
- **Detailed Reporting**: Generates comprehensive reports in CSV format and visualizes coverage with charts.
- **Configurable Depth**: Allows aggregation of fields at specified depths for streamlined reporting.
- **Normalization Option**: Supports case-insensitive comparison of field names.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/pligor/graphql-coverage.git
   cd graphql-coverage
   ```

2. **Install Dependencies**

   Ensure you have Python 3.7 or higher installed. Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

The primary tool is the `graphql_coverage.py` script, which can be executed via the command line. Below is a step-by-step guide to using the script effectively.

### Command-Line Interface

#### Available Options

| Option                     | Description                                                   | Default                         |
| -------------------------- | ------------------------------------------------------------- | ------------------------------- |
| `--schema_path`            | Path to the GraphQL schema file.                              | `GraphQLClients/spaceXplayground/schema.graphql` |
| `--queries_path`           | Path to the directory containing GraphQL queries.             | `GraphQLClients/spaceXplayground/Queries`        |
| `--only_leafs`             | If set, only leaf fields will be considered.                 | `False`                         |
| `--depth`                  | Depth for reporting coverage. Aggregates fields at this level.| `1`                             |
| `--normalize_field_names`  | If set, field names will be normalized (case-insensitive).   | `False`                         |
| `--csv_path`               | Path to the CSV file for the coverage report.                | `schema_coverage_report.csv`    |
| `--plot_path`              | Path to the plot file for the coverage chart.                | `schema_coverage_chart.png`      |

#### Examples

1. **Basic Usage**

   Analyze the default schema and queries directory, extracting all fields:

   ```bash
   python graphql_coverage.py
   ```

2. **Only Leaf Fields**

   Focus the analysis on leaf fields:

   ```bash
   python graphql_coverage.py --only_leafs
   ```

3. **Specify Custom Paths**

   Provide custom paths for the schema and queries:

   ```bash
   python graphql_coverage.py --schema_path path/to/schema.graphql --queries_path path/to/queries/
   ```

4. **Normalize Field Names and Adjust Depth**

   Normalize field names for case-insensitive comparison and aggregate fields at depth 2:

   ```bash
   python graphql_coverage.py --normalize_field_names --depth 2
   ```

5. **Custom Report and Plot Paths**

   Define custom output paths for the CSV report and coverage chart:

   ```bash
   python graphql_coverage.py --csv_path output/report.csv --plot_path output/chart.png
   ```

### Output

Upon execution, the script performs the following steps:

1. **Schema Loading**

   - Loads the entire GraphQL schema from the specified file.
   - Extracts all fields or only leaf fields based on the `--only_leafs` flag.

2. **Query Loading**

   - Recursively searches the specified directory for all `.graphql` query files.
   - Reads each query, storing its file path and content.

3. **Field Usage Extraction**

   - Parses each query, handling fragments, and extracts hierarchical field names.
   - Counts how many queries each field appears in.

4. **Coverage Calculation**

   - Compares the extracted schema fields against the fields used in queries.
   - Calculates the coverage percentage.

5. **Report Generation**

   - Generates a CSV report detailing field usage and coverage.
   - Creates a visual chart representing the coverage.

After successful execution, you will find the `schema_coverage_report.csv` and `schema_coverage_chart.png` in your specified output paths.

## Jupyter Notebook Playground

The repository includes a Jupyter Notebook (`graphql_coverage.ipynb`) that serves as an interactive environment for experimenting with the coverage analysis. While the CLI script is intended for regular use, the notebook provides a deeper dive into each step of the process, leveraging comments and outputs to enhance understanding.

## Contributing

Contributions are welcome! If you encounter issues, have questions, or want to suggest improvements, please [raise an issue](https://github.com/pligor/graphql-coverage/issues) on GitHub.

## License

This project is licensed under the [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.en.html).

## Acknowledgements

Thank you for using GraphQL Coverage! Your feedback and contributions help improve the tool for everyone.
