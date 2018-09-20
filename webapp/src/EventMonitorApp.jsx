import React from 'react';
import ReactDOM from 'react-dom';



//import React from 'react';
import PropTypes from 'prop-types';

export default class Message extends React.Component {
  render() {
    return <label>{ this.props.timesamps_stack }</label>;
  }
}

Message.propTypes = {
  //Failed prop type: The prop `message` is marked as required in `Message`, but its value is `undefined`.
  //message: PropTypes.string.isRequired

  // https://reactjs.org/docs/typechecking-with-proptypes.html
  timesamps_stack: PropTypes.string.isRequired
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

ReactDOM.render(<EventMonitorApp />, document.querySelector('#ra-content'));

/*
names:
    webapp_collector

*/
