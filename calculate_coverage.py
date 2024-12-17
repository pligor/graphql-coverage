def calculate_coverage(schema_fields: set, used_fields: set, normalize: bool = False) -> tuple[float, set, set]:
    """
    Calculates the coverage percentage of schema fields that are used in queries.

    Args:
        schema_fields (set): Set of all hierarchical field names defined in the schema.
        used_fields (set): Set of all hierarchical field names used in queries.
        normalize (bool): If True, convert all field names to lowercase for comparison.

    Returns:
        tuple:
            - float: Coverage percentage.
            - set: Covered fields.
            - set: Uncovered fields.
    """
    if not isinstance(schema_fields, set) or not isinstance(used_fields, set):
        raise TypeError("Both schema_fields and used_fields must be sets.")

    if normalize:
        schema_fields = {field.lower() for field in schema_fields}
        used_fields = {field.lower() for field in used_fields}

    if not schema_fields:
        return 0.0, set(), set()

    covered = schema_fields.intersection(used_fields)
    uncovered = schema_fields.difference(used_fields)
    coverage_percentage = (len(covered) / len(schema_fields)) * 100
    return coverage_percentage, covered, uncovered

if __name__ == "__main__":
  def test_calculate_coverage():
      # Define a set of schema fields
      schema_fields = {
          'user.id',
          'user.name',
          'user.email',
          'user.address.street',
          'user.address.city',
          'user.address.country',
          'post.id',
          'post.title',
          'post.author',
          'comment.id',
          'comment.content',
          'comment.author',
      }

      # Define a set of used fields from queries
      used_fields = {
          'user.id',
          'user.name',
          'user.email',
          'user.address.street',
          'user.address.city',
          'user.address.country',
          'post.title',
          'comment.content',
      }

      # Expected results
      expected_coverage_percentage = (8 / 12) * 100  # 66.67%
      expected_covered_fields = {
          'user.id',
          'user.name',
          'user.email',
          'user.address.street',
          'user.address.city',
          'user.address.country',
          'post.title',
          'comment.content',
      }
      expected_uncovered_fields = {
          'post.id',
          'post.author',
          'comment.id',
          'comment.author',
      }

      # Calculate coverage
      coverage_percentage, covered_fields, uncovered_fields = calculate_coverage(schema_fields, used_fields)

      # Assertions
      assert abs(coverage_percentage - expected_coverage_percentage) < 0.01, "Coverage percentage does not match expected value."
      assert covered_fields == expected_covered_fields, "Covered fields do not match expected fields."
      assert uncovered_fields == expected_uncovered_fields, "Uncovered fields do not match expected fields."

      print("All tests passed!")

  # Run the test
  test_calculate_coverage()