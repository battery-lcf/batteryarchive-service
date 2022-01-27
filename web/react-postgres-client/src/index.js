import React from 'react';
import { ThemeProvider } from '@material-ui/core/styles';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import App from './App';
import Edit from './Edit'
import theme from "./theme";


ReactDOM.render(
    <BrowserRouter>
    <Routes>
     <Route exact path="/" element={<App/>}></Route>
     <Route path="/edit" element={<Edit/>}></Route>
   </Routes>
   </BrowserRouter>,
 document.getElementById('root'));