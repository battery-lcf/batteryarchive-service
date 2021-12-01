from archive_constants import TEST_DB_URL
import connexion
import os
import sys 

app = connexion.FlaskApp(__name__)
app.add_api('/bas/src/app/api/api.yaml') 
app.app.config['DATABASE_URI'] = TEST_DB_URL
app.app.config['DATABASE_CONNECT_OPTIONS'] = {}
print(os.getcwd(), file=sys.stderr)
print(TEST_DB_URL)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='4000')
