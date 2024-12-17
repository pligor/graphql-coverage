from collections import defaultdict

def generate_report(coverage: float, field_usage: defaultdict, schema_fields: set, uncovered_fields: set, depth: int = None,
                    csv_path: str = "schema_coverage_report.csv", plot_path: str = "schema_coverage_chart.png"):
    """
    Generates a comprehensive coverage report.

    Args:
        coverage (float): Overall coverage percentage.
        field_usage (defaultdict): Dictionary mapping field names to their usage counts.
        schema_fields (set): Set of all schema fields.
        uncovered_fields (set): Set of schema fields not covered by any queries.
        depth (int, optional): The depth level for aggregating fields in the plot.
                               - depth=1: Top-level fields (e.g., 'launchesUpcoming')
                               - depth=2: Second-level fields (e.g., 'launchesUpcoming.rocket')
                               - depth=None: No aggregation, plot all fields individually
    """
    import pandas as pd
    import matplotlib.pyplot as plt

    # Print Coverage Summary
    print(f"Schema Coverage: {coverage:.2f}%\n")
    print(f"Total Fields: {len(schema_fields)}")
    print(f"Covered Fields: {len(schema_fields) - len(uncovered_fields)}")
    print(f"Uncovered Fields: {len(uncovered_fields)}\n")

    # Create a DataFrame for detailed report
    data = []
    for field in schema_fields:
        usage = field_usage.get(field, 0)
        data.append({'Field': field, 'Usage Count': usage, 'Covered': field not in uncovered_fields})
    df = pd.DataFrame(data)
    df = df.sort_values(by='Usage Count', ascending=False)

    # Display Detailed Field Usage
    print("Detailed Field Usage:")
    print(df.to_string(index=False))

    # Aggregation Function
    def aggregate_field(field: str, depth: int) -> str:
        parts = field.split('.')
        if depth is None or depth <= 0 or depth > len(parts):
            return field
        return '.'.join(parts[:depth])

    # Prepare Data for Plotting
    if depth is not None:
        # Aggregate fields based on the specified depth
        df['Aggregated Field'] = df['Field'].apply(lambda x: aggregate_field(x, depth))
        aggregated_df = df.groupby('Aggregated Field')['Usage Count'].sum().reset_index()
        
        # Sort aggregated data
        aggregated_df = aggregated_df.sort_values(by='Usage Count', ascending=False)
        
        # Plotting the aggregated coverage
        plt.figure(figsize=(12, 8))
        plt.bar(aggregated_df['Aggregated Field'], aggregated_df['Usage Count'], color='blue')
        plt.title(f'GraphQL Schema Field Usage (Aggregated at Depth {depth})')
        plt.xlabel('Aggregated Fields')
        plt.ylabel('Total Usage Count')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.show()
    else:
        # Plotting the coverage without aggregation (current implementation)
        plt.figure(figsize=(12, 8))

        # Separate covered and uncovered fields
        covered_df = df[df['Covered'] == True]
        uncovered_df = df[df['Covered'] == False]

        # Plot covered fields
        covered_df.plot(kind='bar', x='Field', y='Usage Count', color='green', label='Covered Fields', ax=plt.gca())

        # Plot uncovered fields on the same axis
        if not uncovered_df.empty:
            uncovered_df.plot(kind='bar', x='Field', y='Usage Count', color='red', label='Uncovered Fields', ax=plt.gca())

        plt.title('GraphQL Schema Field Usage')
        plt.xlabel('Fields')
        plt.ylabel('Usage Count')
        plt.legend()
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.show()

    # Optionally, save the DataFrame to a CSV for further analysis
    df.to_csv(csv_path, index=False)
