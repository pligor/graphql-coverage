from typing import Optional
from graphql import SchemaDefinitionNode, DocumentNode, ObjectTypeDefinitionNode
from graphql.language.ast import OperationType
from graphql import parse

def extract_root_types(schema: DocumentNode, debug: bool = False) -> tuple[str, Optional[str]]:
    """
    Extracts the root query and mutation type names from the schema.

    Args:
        schema (DocumentNode): A parsed GraphQL schema represented as a DocumentNode.
        debug (bool): If True, prints debug statements. Defaults to False.

    Returns:
        tuple[str, Optional[str]]: A tuple containing the root query type name and the root mutation type name (if any).

    Raises:
        ValueError: If the schema definition is missing or doesn't define a query type.
    """
    root_query_type: Optional[str] = None
    root_mutation_type: Optional[str] = None

    if debug:
        print("Inspecting schema definitions...")
    for defn in schema.definitions:
        if debug:
            print(f"Definition kind: {defn.kind}, Type: {type(defn)}")
        if isinstance(defn, SchemaDefinitionNode):
            if debug:
                print("Found SchemaDefinitionNode.")
            for op_type in defn.operation_types:
                if debug:
                    print(f"Operation: {op_type.operation}, Type: {op_type.type.name.value}")
                if op_type.operation == OperationType.QUERY:
                    root_query_type = op_type.type.name.value
                elif op_type.operation == OperationType.MUTATION:
                    root_mutation_type = op_type.type.name.value

    # Handle default root types if schema definition is missing
    if not root_query_type:
        # Attempt to use default 'Query' type
        for defn in schema.definitions:
            if isinstance(defn, ObjectTypeDefinitionNode) and defn.name.value == "Query":
                root_query_type = "Query"
                if debug:
                    print("Default root query type 'Query' found.")
                break

    if not root_mutation_type:
        # Attempt to use default 'Mutation' type
        for defn in schema.definitions:
            if isinstance(defn, ObjectTypeDefinitionNode) and defn.name.value == "Mutation":
                root_mutation_type = "Mutation"
                if debug:
                    print("Default root mutation type 'Mutation' found.")
                break

    if not root_query_type:
        available_definitions = [defn.kind for defn in schema.definitions]
        if debug:
            print(f"Available definitions: {available_definitions}")
        raise ValueError("Root query type not found in schema.")

    if debug:
        print(f"Extracted Root Query Type: {root_query_type}")
        print(f"Extracted Root Mutation Type: {root_mutation_type}")

    return root_query_type, root_mutation_type


if __name__ == "__main__":
  def test_extract_root_types_happy_path():
      """
      Tests the happy path for extract_root_types function using a simple schema with Query and Mutation types.
      """
      # Define a minimal test schema
      test_schema = """
      schema {
          query: MyQuery
      }

      type MyQuery {
          testField: String
      }

      type Mutation {
          testMutation: Boolean
      }
      """

      # Parse the schema
      schema_ast = parse(test_schema)

      # Extract root types
      root_query, root_mutation = extract_root_types(schema_ast)

      # Assert the expected values
      assert root_query == "MyQuery", f"Expected root query type to be 'MyQuery', but got '{root_query}'"
      assert root_mutation == "Mutation", f"Expected root mutation type to be 'Mutation', but got '{root_mutation}'"

      # Test with debug=True to ensure it doesn't break the functionality
      root_query_debug, root_mutation_debug = extract_root_types(schema_ast, debug=True)
      assert root_query_debug == root_query, "Debug mode changed the root query type"
      assert root_mutation_debug == root_mutation, "Debug mode changed the root mutation type"

      print("All test assertions passed successfully!")


  test_extract_root_types_happy_path()
