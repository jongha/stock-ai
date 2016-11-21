import React from 'react';
import axios from 'axios';
import {connect} from 'react-redux';
import {Header, Footer} from '../index';

var style = require('./App.less');
var FontAwesome = require('react-fontawesome');

class App extends React.Component {
    constructor(props) {
        super(props);
        this.onClick = this.onClick.bind(this);
    }

    onClick() {
        axios.get('/analytics.json?code=005930').then(response => {
            console.log(response);
            // this.props.onReceive(response.data.number);
        });
    }

    componentDidMount() {
        // this.input.value = 'I used ref to do this';
    }

    componentDidUpdate() {}

    render() {
        console.log(style);

        let text = 'Container'
        return (
            <div className={ style.testtext } onClick={ this.onClick }>
                <Header title={ this.props.headerTitle } />
                {text}
                <div ref={ ref => { this.element = ref } }>
                    {this.props.value}
                </div>

                <Footer />
            </div>
        );
    }
}

App.defaultProps = {
    headerTitle: 'Default header',
    contentTitle: 'Default contentTitle',
    contentBody: 'Default contentBody'
};

export default App;
