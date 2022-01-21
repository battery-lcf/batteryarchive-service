import React, {useState} from 'react';
import "./Edit.css"

function Edit() {
    const [inputField , setInputField] = useState({
        cell_id: '',
        anode: '',
        cathode: '',
        source:'',
        form_factor:'',
        ah:''
    })

    const inputsHandler = e => {
        const {name, value} = e.target;
        setInputField(prevState => ({
          ...prevState,
          [name]: value
        }));
      };

    const submitButton = () =>{
        let anode = inputField.anode 
        let cathode = inputField.cathode
        let source = inputField.source
        let form_factor = inputField.form_factor
        let ah = inputField.ah
        let cell_id = "ulcell_c"

        console.log(anode)
        console.log(cathode)
        fetch('http://34.102.57.101:3001/cell/'+ cell_id, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ anode, cathode, source, form_factor, ah }),
          })
            .then(response => {
              return response.text();
            })
            .catch(function (error) {
              console.warn(error);
            }).finally(function () {
              console.log("edited")
            });
    }

    return (
        <div>

        <div className='edit'> <h2>Edit Cell Metdata</h2></div>   
        
            <input 
        className='edit-form'
        type="text" 
        name="cell_id" 
        onChange={inputsHandler} 
        placeholder="Cell ID" 
        value={inputField.cell_id}/>

        <br/>

        <input 
        className='edit-form'
        type="text" 
        name="anode" 
        onChange={inputsHandler} 
        placeholder="Anode" 
        value={inputField.anode}/>

        <br/>

        <input 
        className='edit-form'
        type="gmail" 
        name="cathode" 
        onChange={inputsHandler} 
        placeholder="Cathode" 
        value={inputField.cathode}/>

        <br/>

        <input 
        className='edit-form'
        type="gmail" 
        name="source" 
        onChange={inputsHandler} 
        placeholder="Source" 
        value={inputField.source}/>

        <br/>

        <input 
        className='edit-form'
        type="gmail" 
        name="form_factor" 
        onChange={inputsHandler} 
        placeholder="Form Factor" 
        value={inputField.form_factor}/>

        <br/>

        <input 
        className='edit-form'
        type="gmail" 
        name="ah" 
        onChange={inputsHandler} 
        placeholder="Amperage" 
        value={inputField.ah}/>

        <br/>

        <button onClick={submitButton} className='submit-edit'>Submit Now</button>
    </div>
    )


}

export default Edit;