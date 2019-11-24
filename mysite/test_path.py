from ..mysite import app
def test_testing():
  assert True
  JSON = app.route_note()
  print(JSON)
