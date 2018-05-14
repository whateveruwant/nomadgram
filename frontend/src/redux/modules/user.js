//imports

//actions

//action creators

//intial state
const intialState = {
    isLoggedIn: localStorage.getItem("jwt") || false
};

//reducer
function reducer(state = intialState, action) {
    switch(action.type) {
        default:
        return state;
    }
};

//reducer functions

//exports

//reducer export
export default reducer;