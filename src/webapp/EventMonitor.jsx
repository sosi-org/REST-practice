import React from 'react';
import ReactDOM from 'react-dom';



import React from 'react';
import PropTypes from 'prop-types';

export default class Message extends React.Component {
  render() {
    return <label>{ this.props.timesamps_stack }</label>;
  }
}

Message.propTypes = {
  message: PropTypes.string.isRequired
}

class EventMonitorApp extends React.Component {
    render() {
        return (
            <div>
            <Message timesamps_stack='Hello React'></Message>
            </div>
        );
    }
}

ReactDOM.render(<EventMonitorApp />, document.querySelector('#content'));

/*
names:
    webapp_collector

*/
