from os.path import isfile, isdir
from load_queries import load_queries
from get_schema_fields import get_schema_fields
from parse_queries_and_extract_fields import parse_queries_and_extract_fields
from calculate_coverage import calculate_coverage
from generate_report import generate_report
from parse_schema import parse_schema
import argparse

SCHEMA_PATH = 'GraphQLClients/spaceXplayground/schema.graphql'
QUERIES_PATH = 'GraphQLClients/spaceXplayground/Queries'
ONLY_LEAFS = False
# When `only_leafs=False`: We extract all fields. This provides a comprehensive list of every field available in the schema, capturing the complete hierarchical structure.
# When `only_leafs=True`: We target only the leaf fields—those that do not have any further sub-fields. This results in a set of terminal fields, omitting intermediate nodes in the hierarchy.
# For the plot, we can aggregate the fields at a certain depth in case we have a large schema.
DEPTH = 1
# When `normalize_field_names=True`: We normalize the field names to do a lowercase comparison.
NORMALIZE_FIELD_NAMES = False
CSV_PATH = "schema_coverage_report.csv"
PLOT_PATH = "schema_coverage_chart.png"

def main(schema_path: str, queries_path: str, only_leafs: bool = False, depth: int = 1, normalize_field_names: bool = False, csv_path: str = "schema_coverage_report.csv", plot_path: str = "schema_coverage_chart.png"):
    assert isfile(schema_path)
    assert isdir(queries_path)

    schema_fields = parse_schema(schema_path=schema_path, only_leafs=only_leafs)
    queries = load_queries(queries_path=queries_path)
    field_usage, used_fields = parse_queries_and_extract_fields(queries=queries, only_leafs=only_leafs)
    assert used_fields.issubset(schema_fields), "All used fields must be defined in the schema"
    coverage_percentage, covered_fields, uncovered_fields = calculate_coverage(schema_fields=schema_fields,
                                                                               used_fields=used_fields,
                                                                               normalize=normalize_field_names)
    generate_report(coverage=coverage_percentage,
                   field_usage=field_usage,
                   schema_fields=schema_fields,
                   uncovered_fields=uncovered_fields,
                   depth=depth,
                   csv_path=csv_path,
                   plot_path=plot_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate GraphQL coverage.")
    parser.add_argument(
        '--schema_path',
        type=str,
        default=SCHEMA_PATH,
        help='Path to the GraphQL schema file.'
    )
    parser.add_argument(
        '--queries_path',
        type=str,
        default=QUERIES_PATH,
        help='Path to the directory containing GraphQL queries.'
    )
    parser.add_argument(
        '--only_leafs',
        action='store_true',
        default=ONLY_LEAFS,
        help='If set, only leaf fields will be considered.'
    )
    parser.add_argument(
        '--depth',
        type=int,
        default=DEPTH,
        help='Depth for reporting coverage.'
    )
    parser.add_argument(
        '--normalize_field_names',
        action='store_true',
        default=NORMALIZE_FIELD_NAMES,
        help='If set, field names will be normalized in the report.'
    )
    parser.add_argument(
        '--csv_path',
        type=str,
        default=CSV_PATH,
        help='Path to the CSV file for the coverage report.'
    )
    parser.add_argument(
        '--plot_path',
        type=str,
        default=PLOT_PATH,
        help='Path to the plot file for the coverage chart.'
    )
    
    args = parser.parse_args()

    main(
        schema_path=args.schema_path,
        queries_path=args.queries_path,
        only_leafs=args.only_leafs,
        depth=args.depth,
        normalize_field_names=args.normalize_field_names,
        csv_path=args.csv_path,
        plot_path=args.plot_path
    )
