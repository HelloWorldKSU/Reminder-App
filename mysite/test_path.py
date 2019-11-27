import app
def test_testing():
  JSON = app._login("test","testpw").user_id
  assert JSON == 0 
