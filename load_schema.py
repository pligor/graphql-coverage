from graphql import parse
from graphql import parse, DocumentNode

from os.path import isfile

SCHEMA_PATH = 'GraphQLClients/spaceXplayground/schema.graphql'

def load_schema(schema_path: str) -> DocumentNode:
    """
    Loads and parses a GraphQL schema from a file.

    Args:
        schema_path (str): The path to the GraphQL schema file.

    Returns:
        DocumentNode: A parsed representation of the GraphQL schema.

    Raises:
        FileNotFoundError: If the schema file does not exist.
        graphql.error.GraphQLError: If the schema cannot be parsed.
    """
    assert isfile(schema_path)
    with open(schema_path, 'r') as file:
        schema_str = file.read()
    return parse(schema_str)

if __name__ == "__main__":
    def test_load_schema_happy_path(schema_path = SCHEMA_PATH):  # Ensure this file exists and is a valid GraphQL schema
      try:
          result = load_schema(schema_path)
          assert isinstance(result, DocumentNode), "Test failed: Result is not a DocumentNode."
          
          # Check for at least one type definition and print its name
          for definition in result.definitions:
              if hasattr(definition, 'name'):
                  print(f"Test passed: Schema loaded successfully with type definition '{definition.name.value}'.")
                  break
          else:
              assert False, "Test failed: No type definitions found in the schema."
      except Exception as e:
          raise AssertionError(f"Test failed with exception: {e}")

    # Run the test
    test_load_schema_happy_path()