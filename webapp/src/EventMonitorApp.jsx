import React from 'react';
import ReactDOM from 'react-dom';


//import DripList from './DripList';


import './EventMonitorApp.css';


//import React from 'react';
import PropTypes from 'prop-types';

// EventBasket
export default class EventBasket extends React.Component {
  render() {
    console.log("EventBasket:", this.props.timesampsstack, typeof this.props.timesampsstack);
    return <label>{ this.props.timesampsstack }</label>;
  }
}

EventBasket.propTypes = {
  //Failed prop type: The prop `message` is marked as required in `EventBasket`, but its value is `undefined`.
  //message: PropTypes.string.isRequired

  // https://reactjs.org/docs/typechecking-with-proptypes.html
  timesampsstack: PropTypes.string.isRequired
}

class EventMonitorApp extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            channel: '',  // username or vicinity whom we are subscribed to. Channel in the sense of Kafka. Filter.
            drips: [],
        };

        // experiment
        this.addDrip = this.addDrip.bind(this);
        this.setupWebsocket = this.setupWebsocket.bind(this);

    }

    componentDidMount() {
        const channel = "bgt";
        this.setState({ channel });

        // You may call setState() immediately in componentDidMount(). It will trigger an extra rendering, but it will happen before the browser updates the screen.

                // call REST APIs using axios
        /*
           axios: https://alligator.io/react/axios-react/
           for API calls
           https://daveceddia.com/ajax-requests-in-react/
        */
        this.setupWebsocket("ws://127.0.0.1:5678/");
    }

    setupWebsocket(ws_address) {
        var ws = new WebSocket(ws_address);

        ws.onopen = function() {
            console.log('connected', ws);
        };
        ws.onerror = function(evt) {
            console.log('ws normal error: ', evt, evt.type);  // evt.type is 'error'  typeof evt.type is string
            var moreinfo = evt.target.url;
            console.log("moreinfo", moreinfo);
            document.getElementById("errors-div").innerHTML = "Cannot connect: " + moreinfo;
             //if (ws.readyState == 1) { }
        };


        let that = this;
        ws.onmessage = function (ws_event) {
            //console.log("onmessage", ws_event);
            let arrival_time = (new Date()).getTime();
            let event_content = JSON.parse(ws_event.data);
            //console.log("received event from Queue", ws_event, event_content);
            event_content.timestamps.push(ws_event.timestamp);
            event_content.timestamps.push(arrival_time);

            //console.log("ws packet content str", ws_event.data);
            //console.log("ws packet content", event_content);
            // assert
            that.addDrip({
                username: event_content.username,
                amount: event_content.amount,
                timestamps: event_content["timestamps"].map(ts => {return ts;}),
            });
        }
    }

    /*
    handleTextChange(e) {
     ...
    }
    */

    /*addFruit(fruit) {
        console.log("fruit added", fruit);
    }
    */
    addDrip(new_drip1) {
        console.log("added drip", new_drip1);
        //this.setState({ drips: [...this.state.chats, data], test: '' });
        var old_drips = this.state.drips;
        var new_drips = old_drips.slice(0); //old_drip.slice(0);
        new_drips.push(new_drip1);
        //this.setState({ drips: new_drips });
        this.setState({drips:new_drips});
        //this.setState({ drips: ["drip A", "drip B"] });
        // this.handleTextChange = this.handleTextChange.bind(this);
        //console.log(this.state);
        console.log(new_drips);

        // "setState() enqueues changes to the component state and tells React that this component and its children need to be re-rendered with the updated state."
        // "Think of setState() as a request rather than an immediate command to update the component."
        // The update may be defered. It is not immediate.
    }


    render() {
        //<EventBasket timesampsstack='Hello React'></EventBasket>
        var k = 0;
        return (
            // style={"background-color": "#eeeeff";}
            <div className="ema">
                <h1>{this.props.channel}</h1>
                <ul>
                    {this.state.drips.map(drip =>
                        // Warning: Each child in an array or iterator should have a unique "key" prop.
                        // <li key={drip.username}>
                        <li key={++k}>£{drip.amount}: {drip.timestamps} ({drip.username}) </li>
                    )}
                </ul>
            </div>
        );
    }
}
/*
based on:
https://daveceddia.com/ajax-requests-in-react/
https://pusher.com/tutorials/react-websockets/
*/

//ReactDOM.render(<EventMonitorApp id="hoho"/>, document.querySelector('#ra-content'));
//console.log("DOM",document.querySelector('#ra-content'));

//addFruit

/*
names:
    webapp_collector
    Message
    EventBasket
    MessageBucket
    Bucket
    EventBasket
*/


/*
class EventBasket extends React.Component  {
    constructor(props) {
    }
}
EventBasket.propTypes = {
  timesamps_stack: PropTypes.string.isRequired
}
*/


function setup_ws(ws_address, messages) {

var ws = new WebSocket(ws_address);
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
    let received_ts = (new Date()).getTime();
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

    //ReactDOM.render(messages, document.querySelector('#messages_ul'))
    //var messages = document.querySelector('#messages_ul');
    messages.appendChild(message2);

    //ReactDOM.render(
    //ReactDOM.render(<EventBasket timesampsstack={""+"message2"} />, document.querySelector('#messages_ul'));
    // React.createElement() learnt from: https://codepen.io/antonietta/pen/KzxxWN?editors=0010#0
    // ---> Warning: React.createElement: type is invalid -- expected a string (for built-in components) or a class/function (for composite components) but got: <EventBasket />. Did you accidentally export a JSX literal instead of a component?
    /*
    React.createElement(
        //<EventBasket timesampsstack={""+"message2"} />,
        //document.querySelector('#messages_ul')
        EventBasket,
        {"timesampsstack": ""+"message2"},
        event_content
    );
    */
    //React.createElement(App, null)

};
}
//} catch(except) {
//document.getElementById("errors-div").innerHTML = "Cannot connect. "+err.message;
//}

ReactDOM.render(<EventMonitorApp channel="hoho"/>, document.querySelector('#ra-content'));
console.log("DOM",document.querySelector('#ra-content'));

/*
var messages_dom = document.createElement('ul');
setup_ws("ws://127.0.0.1:5678/", messages_dom);
document.body.appendChild(messages_dom);
*/
console.log("ready.");
