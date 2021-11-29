from flask import Flask, request
from archive_constants import TEST_DB_URL
from aio import ArchiveWriter
from model import ArchiveOperator
from cell import ArchiveCell

app = Flask(__name__)
app.config['DATABASE_URI'] = TEST_DB_URL
app.config['DATABASE_CONNECT_OPTIONS'] = {}

#TODO: rebuild with OpenAPI


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/export-metadata/<cell_id>/<path>")
def export_celltest_data(cell_id=None, path=None):
    ao = ArchiveOperator()
    cell = ArchiveCell(cell_id)
    df = ao.read_celltest_metadata(cell)
    return ArchiveWriter.write_to_csv(df, cell.cell_id, path,
                                      cell.test_type + "_data")


@app.route("/add")
def addMode():
    app.logger.info('Adding Started')
    #di.main(['-m', 'add', '-p', 'data/snl/'])
    return "<p>Added!</p>"


@app.route("/add-export")
def addAndexportMode():
    app.logger.info('Adding Started')
    #di.main(['-m', 'add', '-p', 'data/snl/'])
    app.logger.info('Export Started')
    #di.main(['-m', 'export', '-p', 'data/snl/'])
    return "<p>Added and Exported</p>"


@app.route("/export")
def exportMode():
    app.logger.info('Export Started')
    #di.main(['-m', 'export', '-p', 'data/snl/'])
    return "<p>Exported</p>"


@app.route("/test-connection")
def testConnection():
    app.logger.info('Testing DB Connection')
    return "<p>DB Connected!</p>"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='4000')
