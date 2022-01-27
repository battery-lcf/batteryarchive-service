import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import "./Edit.css"


function Create() {
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

    const navigate = useNavigate();
  
    const SubmitButton = () =>{
        let anode = inputField.anode 
        let cathode = inputField.cathode
        let source = inputField.source
        let form_factor = inputField.form_factor
        let ah = inputField.ah
        let cell_id = inputField.cell_id
        

        console.log(anode)
        console.log(cathode)
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
            .catch(function (error) {
              console.warn(error);
            }).finally(function () {
              console.log("created")
        });
        navigate('/');

    }

    return (
        <div>

        <div className='edit'> <h2>Create Cell Metdata</h2></div>   
        
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

        <button onClick={SubmitButton} className='submit-edit'>Submit Now</button>
    </div>
    )


}

export default Create;