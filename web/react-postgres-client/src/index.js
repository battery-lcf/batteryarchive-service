import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import App from './App';
import Edit from './Edit'
import Create from './Create'



ReactDOM.render(
    <BrowserRouter>
    <Routes>
     <Route exact path="/" element={<App/>}></Route>
     <Route path="/edit" element={<Edit/>}></Route>
     <Route path="/create" element={<Create/>}></Route>
   </Routes>
   </BrowserRouter>,
 document.getElementById('root'));