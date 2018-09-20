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





var messages = document.createElement('ul');

var ws = new WebSocket("ws://127.0.0.1:5678/");
// How to catch error: https://stackoverflow.com/questions/25779831/how-to-catch-websocket-connection-to-ws-xxxnn-failed-connection-closed-be

ws.onopen = function() {
      console.log('connected');
    };
ws.onerror = function(evt) {
    console.log('ws normal error: ', evt, evt.type);  // evt.type is 'error'  typeof evt.type is string
    var moreinfo = evt.target.url;
    console.log("moreinfo", moreinfo);
    document.getElementById("errors-div").innerHTML = "Cannot connect: " + moreinfo;
     //if (ws.readyState == 1) { }
   };

ws.onmessage = function (ws_event) {
    let received_ts = new Date();
    let event_content = JSON.parse(ws_event.data);
    console.log("received event from Queue", ws_event, event_content);
    event_content.timestamps.push(ws_event.timestamp); // new Date()
    event_content.timestamps.push(received_ts); //


    let message2 = ((event_)=>{
        var message_li = document.createElement('li');
            //content = document.createTextNode(event_.data);
        var timestamps_dom = document.createElement('ol');
        let count = 0;
        event_["timestamps"].forEach( (ts)=>{
            timestamps_dom.appendChild(document.createTextNode(count+":"+ts+" "));
            ++count;
        } );
        /* Ugly old JavaScript
        for (let tsi in event_["timestamps"]) {
            let ts = event_["timestamps"][tsi];
        }
        */
        //console.log("count", count); // 3

        //document.createTextNode(event_.timestamps)
        //message_li.appendChild(content);
        message_li.appendChild(document.createTextNode("Timestamps:"));
        message_li.appendChild(timestamps_dom);
        return message_li;
    })(event_content);

    var messages = document.getElementsByTagName('ul')[0];
    messages.appendChild(message2);
};
document.body.appendChild(messages);
console.log("ready.");
//} catch(except) {
//document.getElementById("errors-div").innerHTML = "Cannot connect. "+err.message;
//}
