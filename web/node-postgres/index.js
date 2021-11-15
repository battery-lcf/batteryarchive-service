const express = require('express')
const app = express()
const port = 3001

const cell_model = require('./cell_model')

app.use(express.json())
app.use(function (req, res, next) {
   res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers');
  next();
});

app.get('/', (req, res) => {
  cell_model.getCells()
  .then(response => {
    res.status(200).send(response);
  })
  .catch(error => {
    res.status(500).send(error);
  })
})
app.post('/cell', (req, res) => {
  cell_model.createCell(req.body)
  .then(response => {
    res.status(200).send(response);
  })
  .catch(error => {
    res.status(500).send(error);
  })
})
app.delete('/cell/:id', (req, res) => {
  cell_model.deleteCell(req.params.id)
  .then(response => {
    res.status(200).send(response);
  })
  .catch(error => {
    res.status(500).send(error);
  })
})
app.put('/cell/:id', (req, res) => {
  cell_model.updateCell(req.params.id, req.body)
  .then(repsonse => {
     res.status(500).send(response)
  })
  .catch(error=> {
     res.status(500).send(error);
  })
})



app.listen(port, () => {
  console.log(`App running on port ${port}.`)
})

