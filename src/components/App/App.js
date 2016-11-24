import React from 'react';
import axios from 'axios';
import ReactDOM from 'react-dom';
import {
    connect
}
from 'react-redux';
import {
    SearchBox,
    AnalyticsBox,
    Header,
    Footer
}
from '../index';

let style = require('./App.less');
let FontAwesome = require('react-fontawesome');

class App extends React.Component {
    constructor(props) {
        super(props);

        this.onSearchBox = this.onSearchBox.bind(this);
        this.onChangeSearchBox = this.onChangeSearchBox.bind(this);
        this.state = {
            analytics: {},
        };
    }

    onSearchBox(e) {
        console.log(e);
        axios.get('/analytics.json?code=005930').then(response => {
            console.log(response);
            this.setState({
                analytics: response.data
            });
        });
    }

    onChangeSearchBox(e) {
        this.setState({
            search: e.target.value
        });
    }

    componentDidMount() {
        console.log('componentDidMount');
    }

    componentDidUpdate() {
        console.log('componentDidUpdate');
    }

    render() {
        return (
            <div className='row'>
                <SearchBox value={ this.state.search } onClick={ this.onSearchBox } onChange={ this.onChangeSearchBox } />
                <AnalyticsBox value={ this.state.analytics } />
            </div>
        );
    }
}

export default App;
