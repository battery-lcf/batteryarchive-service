from archive_constants import DB_URL
import connexion

app = connexion.FlaskApp(__name__)
app.add_api('../api/api.yaml') 
app.app.config['DATABASE_URI'] = DB_URL
app.app.config['DATABASE_CONNECT_OPTIONS'] = {}
print("Connected to database: {}".format(app.app.config['DATABASE_URI']))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='4000')
