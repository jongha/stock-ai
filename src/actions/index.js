export const RECV_VALUE = "RECV_VALUE";

export function receiveValue(value) {
    return {
        type: RECV_VALUE,
        value: value
    };
};