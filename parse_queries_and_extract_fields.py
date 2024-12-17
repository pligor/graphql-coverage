# /Users/gp/Library/CloudStorage/Dropbox/downloads/agile_actors/projs/msTests/GraphQLClients/spaceXplayground/coverage.ipynb
from collections import defaultdict
from graphql import parse, DocumentNode, OperationDefinitionNode, FragmentDefinitionNode
from extract_fields import extract_fields
def parse_queries_and_extract_fields(queries: list, only_leafs: bool = False) -> tuple[defaultdict, set]:
    """
    Parses a list of GraphQL query strings and extracts hierarchical field usage information.

    Args:
        queries (list): A list of tuples, each containing a file path and a GraphQL query string.
        only_leafs (bool): If True, only includes fields without sub-fields (leaf nodes).
                           If False, includes all fields.

    Returns:
        tuple[defaultdict, set]: A tuple containing:
            - defaultdict: A dictionary where keys are hierarchical field names and values are the count of how many GraphQL files each field is used in.
            - set: A set of all unique hierarchical field names used across all queries.
    """
    field_usage = defaultdict(int)
    used_fields = set()

    for file_path, query_str in queries:
        # Temporary set to hold unique fields per file
        temp_used_fields = set()
        try:
            document = parse(query_str)
            # Extract fragments from the current document
            fragments = {definition.name.value: definition 
                         for definition in document.definitions 
                         if isinstance(definition, FragmentDefinitionNode)}
            for definition in document.definitions:
                if isinstance(definition, OperationDefinitionNode):
                    fields = extract_fields(definition, fragments, only_leafs=only_leafs)
                    temp_used_fields.update(fields)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            continue  # Skip this query if there's a parsing error

        # Increment field usage counts based on unique fields in this file
        for field in temp_used_fields:
            field_usage[field] += 1
            used_fields.add(field)

    return field_usage, used_fields

if __name__ == "__main__":
  def test_parse_queries_and_extract_fields_hierarchical():
      """
      Tests the parse_queries_and_extract_fields function to ensure it correctly extracts
      hierarchical field names from GraphQL queries, both including all fields and only leaf fields.
      """
      # Define a concise GraphQL schema as a string (Note: Not used in the function, but kept for reference)
      schema_str = """
      type Query {
          user: User
          post: Post
          comment: Comment
      }

      type User {
          id: ID
          name: String
          address: Address
      }

      type Address {
          street: String
          city: String
          country: String
      }

      type Post {
          id: ID
          title: String
          author: User
      }

      type Comment {
          id: ID
          content: String
          author: User
      }

      fragment AuthorDetails on User {
          id
          name
          address {
              street
              city
              country
          }
      }
      """

      # Define a list of GraphQL queries as strings, including fragment definitions within queries
      queries = [
          ('query1.graphql', '''
          query {
              user {
                  id
                  name
              }
              post {
                  title
              }
          }
          '''),
          ('query2.graphql', '''
          query {
              user {
                  email
              }
              comment {
                  content
              }
              authorDetails: user {
                  ...AuthorDetails
              }
          }

          fragment AuthorDetails on User {
              id
              name
              address {
                  street
                  city
                  country
              }
          }
          ''')
      ]

      # Define the expected field usage and set of used fields when only_leafs=False
      expected_field_usage_all = defaultdict(int, {
          'user': 2,                  # 'user' appears in both queries
          'user.id': 2,
          'user.name': 2,
          'post': 1,
          'post.title': 1,
          'user.email': 1,
          'comment': 1,
          'comment.content': 1,
          'user.address': 1,
          'user.address.street': 1,
          'user.address.city': 1,
          'user.address.country': 1,
      })
      expected_used_fields_all = {
          'user',
          'user.id',
          'user.name',
          'post',
          'post.title',
          'user.email',
          'comment',
          'comment.content',
          'user.address',
          'user.address.street',
          'user.address.city',
          'user.address.country',
      }

      # Define the expected field usage and set of used fields when only_leafs=True
      expected_field_usage_leafs = defaultdict(int, {
          'user.id': 2,
          'user.name': 2,
          'post.title': 1,
          'user.email': 1,
          'comment.content': 1,
          'user.address.street': 1,
          'user.address.city': 1,
          'user.address.country': 1,
      })
      expected_used_fields_leafs = {
          'user.id',
          'user.name',
          'post.title',
          'user.email',
          'comment.content',
          'user.address.street',
          'user.address.city',
          'user.address.country',
      }

      # Call the function to test with only_leafs=False
      field_usage_all, used_fields_all = parse_queries_and_extract_fields(queries, only_leafs=False)

      # Assertions for only_leafs=False
      if field_usage_all != expected_field_usage_all:
          diff_all = {k: (field_usage_all.get(k, 0), expected_field_usage_all.get(k, 0)) 
                      for k in set(field_usage_all) | set(expected_field_usage_all) 
                      if field_usage_all.get(k, 0) != expected_field_usage_all.get(k, 0)}
          raise AssertionError(f"Test failed for all fields. Differences: {diff_all}")

      if used_fields_all != expected_used_fields_all:
          diff_used_all = (used_fields_all - expected_used_fields_all) | (expected_used_fields_all - used_fields_all)
          raise AssertionError(f"Test failed for used fields (all). Differences: {diff_used_all}")

      # Call the function to test with only_leafs=True
      field_usage_leafs, used_fields_leafs = parse_queries_and_extract_fields(queries, only_leafs=True)

      # Assertions for only_leafs=True
      if field_usage_leafs != expected_field_usage_leafs:
          diff_leafs = {k: (field_usage_leafs.get(k, 0), expected_field_usage_leafs.get(k, 0)) 
                        for k in set(field_usage_leafs) | set(expected_field_usage_leafs) 
                        if field_usage_leafs.get(k, 0) != expected_field_usage_leafs.get(k, 0)}
          raise AssertionError(f"Test failed for leaf fields. Differences: {diff_leafs}")

      if used_fields_leafs != expected_used_fields_leafs:
          diff_used_leafs = (used_fields_leafs - expected_used_fields_leafs) | (expected_used_fields_leafs - used_fields_leafs)
          raise AssertionError(f"Test failed for used fields (leafs). Differences: {diff_used_leafs}")

      print("Test passed: Extracted field usage and used fields match the expected hierarchical values.")

  # Run the test
  test_parse_queries_and_extract_fields_hierarchical()
