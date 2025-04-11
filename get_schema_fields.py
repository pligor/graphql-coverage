from graphql.language.ast import (
    ObjectTypeDefinitionNode,
    SchemaDefinitionNode,
    FieldDefinitionNode,
    NamedTypeNode,
    ListTypeNode,
    NonNullTypeNode,
)
from typing import Set, Optional
from extract_root_types import extract_root_types
from graphql import parse, DocumentNode

def get_schema_fields(
    schema: DocumentNode, 
    only_leafs: bool = False, 
    root_query_type: Optional[str] = None,
    root_mutation_type: Optional[str] = None
) -> Set[str]:
    """
    Recursively extracts hierarchical field names from a GraphQL schema, starting from the root Query and Mutation types.

    Args:
        schema (DocumentNode): A parsed GraphQL schema represented as a DocumentNode.
        only_leafs (bool): If True, only returns fields that don't have sub-fields (leaf nodes).
                           If False, returns all fields including intermediate nodes.
        parent_path (str): The hierarchical path of the parent field.
        root_query_type (Optional[str]): Name of the root query type. If None, defaults to extracting from schema.
        root_mutation_type (Optional[str]): Name of the root mutation type. If None, defaults to extracting from schema.

    Returns:
        Set[str]: A set of hierarchical field names from the schema, filtered based on the only_leafs parameter.

    Raises:
        ValueError: If the root query type is not found in the schema.
    """
    fields = set()
    type_definitions = {
        d.name.value: d for d in schema.definitions if isinstance(d, ObjectTypeDefinitionNode)
    }

    # Extract root types if not provided
    if root_query_type is None or root_mutation_type is None:
        _root_query_type, _root_mutation_type = extract_root_types(schema)
    else:
        _root_query_type = root_query_type
        _root_mutation_type = root_mutation_type

    if _root_query_type not in type_definitions:
        raise ValueError(f"Root query type '{_root_query_type}' not found in schema.")

    def get_named_type(node):
        if isinstance(node, NonNullTypeNode) or isinstance(node, ListTypeNode):
            return get_named_type(node.type)
        elif isinstance(node, NamedTypeNode):
            return node.name.value
        return None

    def extract_fields_from_type(
        type_name: str, current_path: str, visited: Set[str] = None
    ) -> Set[str]:
        if visited is None:
            visited = set()

        if type_name in visited:
            return set()

        visited.add(type_name)
        type_def = type_definitions.get(type_name)

        if not type_def:
            return set()

        for field in type_def.fields:
            field_name = field.name.value
            field_type = get_named_type(field.type)
            has_subfields = field_type in type_definitions

            hierarchical_field = f"{current_path}.{field_name}" if current_path else field_name

            # Add field based on only_leafs parameter
            if not only_leafs or (only_leafs and not has_subfields):
                fields.add(hierarchical_field)

            # Recursively process subfields using a fresh copy of visited for each branch
            if has_subfields:
                extract_fields_from_type(field_type, hierarchical_field, visited.copy())

        return fields

    # Process Query type
    query_type_def = type_definitions[_root_query_type]
    for field in query_type_def.fields:
        field_name = field.name.value
        field_type = get_named_type(field.type)
        has_subfields = field_type in type_definitions

        hierarchical_field = field_name

        # Add field based on only_leafs parameter
        if not only_leafs or (only_leafs and not has_subfields):
            fields.add(hierarchical_field)

        # Recursively get subfields
        if has_subfields:
            extract_fields_from_type(field_type, hierarchical_field)

    # Optionally, handle Mutation type if exists
    if _root_mutation_type and _root_mutation_type in type_definitions:
        mutation_type_def = type_definitions[_root_mutation_type]
        for field in mutation_type_def.fields:
            field_name = field.name.value
            field_type = get_named_type(field.type)
            has_subfields = field_type in type_definitions

            hierarchical_field = field_name

            # Add field based on only_leafs parameter
            if not only_leafs or (only_leafs and not has_subfields):
                fields.add(hierarchical_field)

            # Recursively get subfields
            if has_subfields:
                extract_fields_from_type(field_type, hierarchical_field)

    return fields

if __name__ == "__main__":
  def test_get_schema_fields_happy_path():
      """
      Tests the get_schema_fields function to ensure it correctly extracts hierarchical field names
      from a simple GraphQL schema, both including all fields and only leaf fields.
      """
      # Define a simple generic GraphQL schema as a string
      schema_str = """
      schema {
        query: Query
        mutation: MyMutation
      }

      type Query {
        book(id: ID!): Book
      }

      type MyMutation {
        addBook(title: String!): Book
      }

      type Book {
        id: ID!
        title: String
        author: Author
      }

      type Author {
        id: ID!
        name: String
      }
      """

      # Parse the schema string into a DocumentNode
      schema: DocumentNode = parse(schema_str)

      # Extract root types
      root_query_type, root_mutation_type = extract_root_types(schema)

      # Define expected fields for both scenarios
      expected_fields_all = {
          # Query fields
          "book",
          "book.id",
          "book.title",
          "book.author",
          "book.author.id",
          "book.author.name",
          # Mutation fields
          "addBook",
          "addBook.id",
          "addBook.title",
          "addBook.author",
          "addBook.author.id",
          "addBook.author.name"
      }

      expected_fields_leafs = {
          # Query leaf fields
          "book.id",
          "book.title",
          "book.author.id",
          "book.author.name",
          # Mutation leaf fields
          "addBook.id",
          "addBook.title",
          "addBook.author.id",
          "addBook.author.name"
      }

      # Extract fields with only_leafs=False
      fields_all = get_schema_fields(
          schema, 
          only_leafs=False, 
          root_query_type=root_query_type, 
          root_mutation_type=root_mutation_type
      )
      missing_fields = expected_fields_all - fields_all
      extra_fields = fields_all - expected_fields_all
      assert fields_all == expected_fields_all, (
          f"Test failed for all fields:\n"
          f"Missing fields: {missing_fields}\n"
          f"Unexpected extra fields: {extra_fields}"
      )

      # Extract fields with only_leafs=True
      fields_leafs = get_schema_fields(
          schema, 
          only_leafs=True, 
          root_query_type=root_query_type, 
          root_mutation_type=root_mutation_type
      )
      missing_leaf_fields = expected_fields_leafs - fields_leafs
      extra_leaf_fields = fields_leafs - expected_fields_leafs
      assert fields_leafs == expected_fields_leafs, (
          f"Test failed for leaf fields:\n"
          f"Missing fields: {missing_leaf_fields}\n"
          f"Unexpected extra fields: {extra_leaf_fields}"
      )

      print("Test passed: Both all fields and leaf-only fields were extracted correctly.")

  # Run the test
  test_get_schema_fields_happy_path()