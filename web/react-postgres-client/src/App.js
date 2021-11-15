import React, {useState, useEffect} from 'react';
import { useTable, useFilters, useGlobalFilter } from "react-table";
import MaUTable from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";


function App() {
  const [cell_data, setCells] = useState([]);
  useEffect(() => {
    getCell();
     	  
  }, [cell_data]);
  function handleErrors(response) {
    if (!response.ok) throw Error(response.statusText);
    return response;
  } 
  function getCell() {
    fetch('http://34.102.57.101:3001/')
      .then(response => {       
        return response.text();
      })
      .then(local_data => {
	let l_data = JSON.parse(local_data);
        setCells(l_data);     
      });
  }
  function createCell() {
    let cell_id = prompt('Enter  cell_id');
    let anode = prompt('Enter anode');
    let cathode = prompt('Enter cathode');
    let source  = prompt('Enter source');
    let form_factor = prompt('Enter form fatcor')
    let ah = prompt('Enter amp hours')
    fetch('http://34.102.57.101:3001/cell', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({cell_id, anode, cathode, source, form_factor, ah }),
    })
      .then(response => {
	
        return response.text();
      })
      .then(data => {
        alert(data);
        getCell();
      });
  }
  function editCell(cell_id) {
    let anode = prompt('Enter anode');
    let cathode = prompt('Enter cathode');
    let source  = prompt('Enter source');
    let form_factor = prompt('Enter form fatcor')
    let ah = prompt('Enter amp hours')
    fetch('http://34.102.57.101:3001/cell/'+cell_id, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ anode, cathode, source, form_factor, ah }),
    })
      .then(response => {
        return response.text();
      })
      .then(data => {
        alert(data);
        getCell();
      });
  }	
  function deleteCell() {
    let id = prompt('Confirm that you want to delete this cell_id by retyping');

    fetch(`http://34.102.57.101:3001/cell/${id}`, {
      method: 'DELETE',
    })
      .then(response => {
        return response.text();
      })
      .then(data => {
        alert(data);
        getCell();
      });
  }
  const columns = [
  {
    Header: "Cell Metadata Table",
    columns: [
      {
        Header: "Cell_ID",
        accessor: "cell_id"
      },
      {
        Header: "Anode",
        accessor: "anode"
      },
           {
        Header: "Cathode",
        accessor: "cathode"
      },
      {
        Header: "Source",
        accessor: "source"
      },
      {
        Header: "Form Factor",
        accessor: "form_factor"
      },
      {
        Header: "Amp Hours",
        accessor: "ah"
      },
       {
        Header: "Edit/Delete",
        Cell: ({ cell }) => ( <>
        <button onClick={() => editCell(cell.row.values.cell_id)}>     
          {"Edit"}
        </button>
        <button onClick={deleteCell}>
          {"Delete"}
        </button>
        </>
        )
      },

    ]
  },
];

const DefaultColumnFilter = ({
  column: { filterValue, preFilteredRows, setFilter }
}) => {
  const count = preFilteredRows.length;

  return (
    <input
      value={filterValue || ""}
      onChange={e => {
        setFilter(e.target.value || undefined);
      }}
      placeholder={`Search ${count} records...`}
    />
  );
};

const GlobalFilter = ({
  preGlobalFilteredRows,
  globalFilter,
  setGlobalFilter
}) => {
  const count = preGlobalFilteredRows && preGlobalFilteredRows.length;

  return (
    <span>
      Search:{" "}
      <input
        value={globalFilter || ""}
        onChange={e => {
          setGlobalFilter(e.target.value || undefined); // Set undefined to remove the filter entirely
        }}
        placeholder={`${count} records...`}
        style={{
          border: "0"
        }}
      />
    </span>
  );
};



const Table = ({ columns, data }) => {
  const filterTypes = React.useMemo(
    () => ({
      text: (rows, id, filterValue) => {
        return rows.filter(row => {
          const rowValue = row.values[id];
          return rowValue !== undefined
            ? String(rowValue)
                .toLowerCase()
                .startsWith(String(filterValue).toLowerCase())
            : true;
        });
      }
    }),
    []
  );

  const defaultColumn = React.useMemo(
    () => ({
      Filter: DefaultColumnFilter
    }),
    []
  );
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    state,
    visibleColumns,
    preGlobalFilteredRows,
    setGlobalFilter
  } = useTable(
    {
      columns,
      data,
      defaultColumn,
      filterTypes
    },
    useFilters,
    useGlobalFilter
  );
  return (
    <MaUTable {...getTableProps()}>
      <TableHead>
        {headerGroups.map(headerGroup => (
          <TableRow {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map(column => (
              <TableCell {...column.getHeaderProps()}>
                {column.render("Header")}
		 <div>{column.canFilter ? column.render("Filter") : null}</div>
              </TableCell>
            ))}
          </TableRow>
        ))}
	<TableRow>
          <TableCell
            colSpan={visibleColumns.length}
            style={{
              textAlign: "left"
            }}
          >
            <GlobalFilter
              preGlobalFilteredRows={preGlobalFilteredRows}
              globalFilter={state.globalFilter}
              setGlobalFilter={setGlobalFilter}
            />
          </TableCell>
        </TableRow>  
      </TableHead>
      <TableBody {...getTableBodyProps()}>
        {rows.map((row, i) => {
          prepareRow(row);
          return (
            <TableRow {...row.getRowProps()}>
              {row.cells.map(cell => {
                return (
                  <TableCell {...cell.getCellProps()}>
                    {cell.render("Cell")}
                  </TableCell>
                );
              })}
            </TableRow>
          );
        })}
      </TableBody>
    </MaUTable>
  );
};

	
  return (
<>	  
    <div>
	   <Table columns={columns} data={cell_data} /> 
    </div>
    <div>
	<button onClick={createCell}>
          {"Create"}
        </button>
    </div>	  
</>
  );
}
export default App;
