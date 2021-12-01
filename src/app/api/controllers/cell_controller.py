from api.py.openapi_client.model.cell import Cell


def get_cells(): 
    """get_cell
    Gets a cell
    :rtype: Cell
    """
    # QUERY DB FOR ALL CELLS
    cell = Cell(
        id=1234
    )
    return cell.id, 200
