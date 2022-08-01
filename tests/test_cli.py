# def test_db_create(runner):
#     result = runner.invoke(args=["db", "create_db"])
#     assert 'Database created' in result.output
#
# def test_db_import(runner):
#     result = runner.invoke(args=["db", "import_authors", "authors.csv"])
#     assert 'objects imported to database' in result.output