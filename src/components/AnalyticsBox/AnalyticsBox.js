import React from 'react';
import axios from 'axios';
import {
    connect
}
from 'react-redux';

let style = require('./AnalyticsBox.less');

class AnalyticsBox extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {}

    componentDidUpdate() {}

    render() {
        return (
            <div>
                { JSON.stringify(this.props.value) }
            </div>
        );
    }
}

export default AnalyticsBox;
