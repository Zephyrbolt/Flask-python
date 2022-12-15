try:
    from flask import Flask
    import requests
    import unittest
    import logging
    from script import home
except Exception as e:
    print("Modules are missing {}".format(e))

def test_base_route():
    app = Flask(__name__)
    home(app) 
    client = app.test_client()
    Url ='/'
    response  = client.get(Url)
    assert response.status_code == 200

class ApiTest(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"


    def testurl(self):
        response = requests.get(self.URL)
        try:
            self.assertEqual(response.status_code, 200)
            logging.info("Test OK")
            print("The test has been passed. The status code is:", response.status_code)
        except AssertionError as e:
            logging.error("Status code mismatch error")
            print("Status codes doesn't match {}".format(e))
            




if __name__ == "__main__":
    unittest.main()
