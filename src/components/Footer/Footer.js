import React from 'react';
import axios from 'axios';
import {connect} from 'react-redux';

var style = require("!css-loader!less-loader!./Footer.less");
var FontAwesome = require('react-fontawesome');

class Footer extends React.Component {
    render() {
        return (
            <h1>Footer</h1>
        );
    }
}

export default Footer;
