import React from 'react';
import { ThemeProvider } from '@material-ui/core/styles';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Switch } from "react-router-dom";
import App from './App';
import Edit from './Edit'
import theme from "./theme";


ReactDOM.render(
    <BrowserRouter>
    <Switch>
     <Route exact path="/" component={App} />
     <Route path="/edit" component={Edit} />
   </Switch>
   </BrowserRouter>,
 document.getElementById('root'));