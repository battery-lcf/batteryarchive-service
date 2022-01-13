const Pool = require('pg').Pool
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'postgres',
  password: 'Qylb0WmyXYLsNZsmgxxNx5QiilEfnl63',
  port: 5432,
})
const getCells = () => {
  return new Promise(function(resolve, reject) {
    pool.query('SELECT * FROM cell_metadata ORDER BY cell_id', (error, results) => {
      if (error) {
        reject(error)
      }
      resolve(results.rows);
    })
  }) 
}
const createCell = (body) => {
  return new Promise(function(resolve, reject) {
    const { cell_id, anode, cathode, source, form_factor, ah } = body
    pool.query('INSERT INTO cell_metadata (cell_id, anode, cathode, source, form_factor, ah) VALUES ($1, $2, $3, $4, $5, $6)  RETURNING *', [cell_id, anode, cathode, source, form_factor, ah], (error, results) => {
      if (error) {
        reject(error)
      }
      resolve(results)
      console.log('New cell added with cell_id :' + cell_id)
    })
  })
}
const deleteCell = (cell_id) => {
  return new Promise(function(resolve, reject) {
    const id = cell_id
    pool.query('DELETE FROM cell_metadata WHERE cell_id = $1', [id], (error, results) => {
      if (error) {
        reject(error)
      }
      resolve(results)
      console.log('Cell deleted with cell_id: ' + cell_id)
    })
  })
}
const updateCell = (cell_id, body) => {
 return new Promise(function(resolve,reject) {
  const id = cell_id
  const { anode, cathode, source, form_factor, ah } = body

  pool.query(
    'UPDATE cell_metadata SET anode= $1, cathode= $2, source= $3, form_factor= $4, ah = $5 WHERE cell_id = $6',
    [ anode, cathode, source, form_factor, ah, id],
    (error, results) => {
      if (error) {
        reject(error)
      }
      resolve(results)
	console.log('Cell edited with cell_id: ' + cell_id) 
    }
  )
 })
}
module.exports = {
  getCells,
  createCell,	
  deleteCell,
  updateCell
}
