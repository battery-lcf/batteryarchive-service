from src.app.model import ArchiveOperator

def get_cells(): 
    """get_cell
    Gets all cells
    :rtype: list of Cell
    """
    ao = ArchiveOperator()
    archive_cells = ao.get_all_cells()
    result = [cell.to_dict() for cell in archive_cells]
    return result, 200

def get_cell_with_id(cell_id): 

    ao = ArchiveOperator()
    archive_cells = [ao.get_cell_with_id(cell_id)]
    result = [cell.to_dict() for cell in archive_cells]
    return result, 200