import React from 'react';
import axios from 'axios';
import {
    connect
}
from 'react-redux';

let style = require('./SearchBox.less');
let FontAwesome = require('react-fontawesome');

class SearchBox extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {}

    componentDidUpdate() {}

    render() {
        return (
            <div>
                <div className='col-md-3'></div>
                <div className='col-md-6'>
                    <div>
                        <div className='input-group col-md-12'>
                            <input type='text' className='form-control input-lg' placeholder={ this.props.placeholder } onChange={ this.props.onChange } value={ this.props.value } />
                            <span className='input-group-btn'>
                                <button className='btn btn-info btn-lg' type='button' onClick={ () => this.props.onClick(this.props.value) }>
                                    <i className='glyphicon glyphicon-search'></i>
                                </button>
                            </span>
                        </div>
                    </div>
                </div>
                <div className='col-md-3'></div>
            </div>
        );
    }
}

SearchBox.defaultProps = {
    placeholder: 'Search',
    value: '005930',
};

// https://facebook.github.io/react/docs/components-and-props.html
// SearchBox.propTypes = {
//     placeholder: React.PropTypes.string,
//     placeholder: React.PropTypes.string.isRequired
// };

export default SearchBox;
