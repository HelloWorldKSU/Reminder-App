import sys
print sys
sys.path.append('~/mysite')
import app
def test_testing():
  assert True
  JSON = app.route_note()
  print(JSON)
