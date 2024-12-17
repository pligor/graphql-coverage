import glob
import os

QUERIES_PATH = 'GraphQLClients/spaceXplayground/Queries'

def load_queries(queries_path: str) -> list:
    """
    Loads and reads all GraphQL query files from a specified directory.

    Args:
        queries_path (str): The path to the directory containing GraphQL query files.

    Returns:
        list: A list of tuples, each containing the file path and the content of a GraphQL query file.

    Raises:
        FileNotFoundError: If no GraphQL query files are found in the specified directory.
    """
    query_files = glob.glob(os.path.join(queries_path, '**', '*.graphql'), recursive=True)
    if not query_files:
        raise FileNotFoundError(f"No GraphQL query files found in directory: {queries_path}")
    
    queries = []
    for file_path in query_files:
        with open(file_path, 'r') as file:
            queries.append((file_path, file.read()))
    return queries

if __name__ == "__main__":
    def test_load_queries_happy_path(queries_path = QUERIES_PATH):
      """
      Tests the load_queries function with a valid queries path.
      """
      try:
          queries = load_queries(queries_path)
          assert queries, "Test failed: No queries loaded."
          assert len(queries) > 0, "Test failed: Empty queries list returned."
          assert all(isinstance(q, tuple) and len(q) == 2 for q in queries), "Test failed: Invalid query format."
          print(f"Test passed: Loaded {len(queries)} queries successfully.")
      except Exception as e:
          raise AssertionError(f"Test failed with exception: {e}")

    # Run the test
    test_load_queries_happy_path()