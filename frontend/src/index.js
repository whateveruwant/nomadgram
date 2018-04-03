import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { ConnectedRouter } from "react-router-redux";
import store, { history } from 'redux/configureStore';
import App from 'components/App/index';
import I18n from 'redux-i18n';
import { translations } from "translations";

// console.log(store.getState());
// store.dispatch({type:"FUCKING"});

ReactDOM.render(
    <Provider store={store}>
        <ConnectedRouter history={history}>
            <I18n translations={translations} initialLang="en" fallbackLang="en">
                <App />
            </I18n>
        </ConnectedRouter>
    </Provider>,
    document.getElementById("root")
);

// localStorage.setItem("bestCourse", "nomad academy");
