from graphql.language.ast import (
    OperationDefinitionNode,
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    InlineFragmentNode,
)
from typing import Set, Dict


def extract_fields(
    node: OperationDefinitionNode,
    fragments: Dict[str, FragmentDefinitionNode],
    parent_path: str = "",
    only_leafs: bool = False,
    verbose: bool = False,
) -> Set[str]:
    """
    Extracts hierarchical fields from a given GraphQL AST node, including nested fields and fragments.

    Args:
        node (OperationDefinitionNode): The GraphQL AST node representing the operation (query, mutation, etc.).
        fragments (Dict[str, FragmentDefinitionNode]): A dictionary of fragment definitions.
        parent_path (str): The hierarchical path of the parent field.
        only_leafs (bool): If True, only includes fields without sub-fields (leaf nodes).
        verbose (bool): If True, prints debug statements.

    Returns:
        Set[str]: A set of hierarchical field names extracted from the node.
    """
    fields = set()

    def traverse_selection(selection, current_path):
        if isinstance(selection, FieldNode):
            field_name = selection.name.value
            hierarchical_field = f"{current_path}.{field_name}" if current_path else field_name
            has_subfields = selection.selection_set is not None

            if verbose:
                print(f"Processing Field: {hierarchical_field} (Has subfields: {has_subfields})")

            # Add field based on only_leafs parameter
            if not only_leafs or (only_leafs and not has_subfields):
                fields.add(hierarchical_field)

            # Recursively process subfields
            if has_subfields:
                for sub_selection in selection.selection_set.selections:
                    traverse_selection(sub_selection, hierarchical_field)

        elif isinstance(selection, FragmentSpreadNode):
            fragment_name = selection.name.value
            if verbose:
                print(f"Processing Fragment Spread: {fragment_name}")
            fragment = fragments.get(fragment_name)
            if fragment:
                for frag_selection in fragment.selection_set.selections:
                    traverse_selection(frag_selection, current_path)  # Use current_path to maintain hierarchy
            else:
                if verbose:
                    print(f"Fragment '{fragment_name}' not found.")

        elif isinstance(selection, InlineFragmentNode):
            type_condition = (
                selection.type_condition.name.value if selection.type_condition else "UnknownType"
            )
            if verbose:
                print(f"Processing Inline Fragment on {type_condition}")
            for inline_selection in selection.selection_set.selections:
                traverse_selection(inline_selection, current_path)  # Use current_path to maintain hierarchy

        else:
            if verbose:
                print(f"Unknown selection type: {type(selection)}")

    for selection in node.selection_set.selections:
        traverse_selection(selection, parent_path)

    return fields


from graphql import parse, DocumentNode
from collections import defaultdict


if __name__ == "__main__":
  def test_extract_fields_hierarchical():
      """
      Tests the extract_fields function to ensure it correctly extracts hierarchical field names
      from GraphQL queries, both including all fields and only leaf fields.
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

      fragment AuthorDetails on Author {
          name
      }
      """

      # Define a simple GraphQL query string
      query_str_all_fields = """
      query {
          book {
              title
              author {
                  name
              }
          }
      }
      """

      # Define a GraphQL query string with a fragment
      query_str_with_fragment = """
      query {
          book {
              title
              author {
                  ...AuthorDetails
              }
          }
      }
      """

      # Parse the schema and queries into DocumentNodes
      schema: DocumentNode = parse(schema_str)
      query_all_fields = parse(query_str_all_fields)
      query_with_fragment = parse(query_str_with_fragment)

      # Extract fragments from the schema
      fragments = {
          definition.name.value: definition
          for definition in schema.definitions
          if isinstance(definition, FragmentDefinitionNode)
      }

      # Extract operation definitions from the queries
      operations = [
          definition
          for definition in query_all_fields.definitions
          if isinstance(definition, OperationDefinitionNode)
      ]

      operations_with_fragment = [
          definition
          for definition in query_with_fragment.definitions
          if isinstance(definition, OperationDefinitionNode)
      ]

      # Combine all operations for testing
      all_operations = operations + operations_with_fragment

      # Define expected fields for both scenarios
      expected_fields_all = {
          "book",
          "book.title",
          "book.author",
          "book.author.name",
      }

      expected_fields_leafs = {
          "book.title",
          "book.author.name",
      }

      # Aggregate extracted fields
      extracted_fields_all = set()
      extracted_fields_leafs = set()

      # Extract fields with only_leafs=False
      for operation in all_operations:
          fields = extract_fields(
              operation, fragments, parent_path="", only_leafs=False, verbose=False
          )
          extracted_fields_all.update(fields)

      # Extract fields with only_leafs=True
      for operation in all_operations:
          fields = extract_fields(
              operation, fragments, parent_path="", only_leafs=True, verbose=False
          )
          extracted_fields_leafs.update(fields)

      # Assertions for only_leafs=False
      assert (
          extracted_fields_all == expected_fields_all
      ), f"Test failed for all fields: Expected {expected_fields_all}, but got {extracted_fields_all}"

      # Assertions for only_leafs=True
      assert (
          extracted_fields_leafs == expected_fields_leafs
      ), f"Test failed for leaf fields: Expected {expected_fields_leafs}, but got {extracted_fields_leafs}"

      print("Test passed: Both all fields and leaf-only fields were extracted correctly.")

  # Run the test
  test_extract_fields_hierarchical()