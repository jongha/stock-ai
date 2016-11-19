import { RECV_VALUE } from '../actions';

const initialState = {
    value: -1
};

const counterReducer = (state = initialState, action) => {
    switch(action.type) {
        case RECV_VALUE:
            return Object.assign({}, state, {
                value: action.value
            });
        default:
            return state;
    }
};

export default counterReducer;
