import React from 'react';
import axios from 'axios';
import {connect} from 'react-redux';

var style = require("!css-loader!less-loader!./Header.less");
var FontAwesome = require('react-fontawesome');

class Header extends React.Component {
    render() {
        return (
            <h1>{ this.props.title }</h1>
        );
    }
}

// https://facebook.github.io/react/docs/components-and-props.html
Header.propTypes = {
    // title: React.PropTypes.string,
    title: React.PropTypes.string.isRequired
};

export default Header;
