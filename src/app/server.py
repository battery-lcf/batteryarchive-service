from flask import Flask, request
from archive_constants import TEST_DB_URL
from aio import ArchiveWriter
from model import ArchiveOperator
from cell import ArchiveCell
import connexion

app = connexion.FlaskApp(__name__)
app.add_api('/bas/src/app/api/api.yaml')
# app.config['DATABASE_URI'] = TEST_DB_URL
# app.config['DATABASE_CONNECT_OPTIONS'] = {}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='4000')
