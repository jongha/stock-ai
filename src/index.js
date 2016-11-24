import React from 'react';
import ReactDOM from 'react-dom';
import { App } from './components';

import { createStore } from 'redux';
import { Provider } from 'react-redux';
import counterReducer from './reducers';

ReactDOM.render(
    <App />,
    document.getElementById('app')
);
