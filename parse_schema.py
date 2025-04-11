from load_schema import load_schema
from extract_root_types import extract_root_types
from get_schema_fields import get_schema_fields
from graphql import parse, DocumentNode
import os

def parse_schema(schema_path: str, only_leafs: bool = False) -> set:
    """
    Parses a GraphQL schema file and extracts field names recursively.

    Args:
        schema_path (str): The file path to the GraphQL schema.
        only_leafs (bool): If True, only returns fields that don't have sub-fields.
                           If False, returns all fields including intermediate nodes.

    Returns:
        set: A set of field names from the schema, filtered based on the only_leafs parameter.
    """
    schema = load_schema(schema_path)
    root_query_type, root_mutation_type = extract_root_types(schema)
    schema_fields = get_schema_fields(
        schema, only_leafs,
        root_query_type=root_query_type,
        root_mutation_type=root_mutation_type
    )
    return schema_fields


if __name__ == "__main__":
  def test_parse_schema_happy_path():
      """
      Tests the parse_schema function to ensure it correctly extracts hierarchical field names
      from a GraphQL schema, both including all fields and only leaf fields.
      """
      # Define a concise GraphQL schema as a string
      schema_str = """
      type Query {
          book: Book
      }

      type Book {
          title: String
          author: Author
      }

      type Author {
          name: String
      }
      """

      # Write the schema to a temporary file
      schema_file_path = 'temp_schema.graphql'
      with open(schema_file_path, 'w') as schema_file:
          schema_file.write(schema_str)

      try:
          # Test with only_leafs=False (include all fields)
          fields_all = parse_schema(schema_file_path, only_leafs=False)
          expected_fields_all = {
              "book",
              "book.title",
              "book.author",
              "book.author.name",
          }
          assert fields_all == expected_fields_all, f"Test failed for all fields: Expected {expected_fields_all}, but got {fields_all}"

          # Test with only_leafs=True (only fields without children)
          fields_leafs = parse_schema(schema_file_path, only_leafs=True)
          expected_fields_leafs = {
              "book.title",
              "book.author.name",
          }
          assert fields_leafs == expected_fields_leafs, f"Test failed for leaf fields: Expected {expected_fields_leafs}, but got {fields_leafs}"

          print("Test passed: Both all fields and leaf-only fields were extracted correctly.")
      finally:
          # Clean up the temporary file
          os.remove(schema_file_path)

  def test_parse_schema_multiple_ref_same_type():
      """Tests that parse_schema correctly extracts fields when the same type is referenced in different branches."""
      schema_str = """
      schema {
          query: Query
      }

      type Query {
          test: TestType
      }

      type TestType {
          x: R
          y: R
      }

      type R {
          a: String
          b: String
      }
      """
      schema_file_path = 'temp_schema2.graphql'
      with open(schema_file_path, 'w') as schema_file:
          schema_file.write(schema_str)
      try:
          # Test with only_leafs=False (include all fields)
          fields_all = parse_schema(schema_file_path, only_leafs=False)
          expected_fields_all = {
              "test",
              "test.x",
              "test.x.a",
              "test.x.b",
              "test.y",
              "test.y.a",
              "test.y.b",
          }
          assert fields_all == expected_fields_all, f"Test failed for all fields: expected {expected_fields_all}, got {fields_all}"

          # Test with only_leafs=True (only fields without children)
          fields_leafs = parse_schema(schema_file_path, only_leafs=True)
          expected_fields_leafs = {
              "test.x.a",
              "test.x.b",
              "test.y.a",
              "test.y.b",
          }
          assert fields_leafs == expected_fields_leafs, f"Test failed for leaf fields: expected {expected_fields_leafs}, got {fields_leafs}"

          print("Test passed: Multiple references to the same type are handled correctly.")
      finally:
          os.remove(schema_file_path)

  # Run the test
  test_parse_schema_happy_path()
  # Run the new test
  test_parse_schema_multiple_ref_same_type()