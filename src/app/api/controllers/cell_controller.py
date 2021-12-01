from api.py.openapi_client.model.cell import Cell
from model import ArchiveOperator

def get_cells(): 
    """get_cell
    Gets all cells
    :rtype: Cell
    """
    ao = ArchiveOperator()
    cells = ao.get_all_cells()
    return len(cells), 200
