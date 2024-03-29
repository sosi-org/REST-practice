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


// Only one default export allowed per module.  `export default class ...`
export class TimestampList1 extends React.Component {
    constructor(props) {
        super(props);
        /*this.state = {
            ts: ''
        };*/
    }
    render() {
        function left0(i) {
            return (("000"+i).slice(-2));
        }
        function date_formatter(d) {
            //return d.getYear()+"/"+d.getMonth()+"/"+d.getDay();
            return left0(d.getHours())+""+d.getMinutes()+":"+left0(d.getSeconds());
            //+left0(d.getMilliseconds());
        }

        // why this.state does not work? this.probs works
        let tslist = this.props.tslist;
        //console.log(tslist);
        let key = 0;
        return tslist.map(ts=>{
            ++key;
            const css = {backgroundColor: '#eeeeff', fontSize: 9};
            return (
                <span key={key}>(<span style={css}> {ts?date_formatter(new Date(ts)):"-"}</span>)&nbsp;</span>
           );
       });
    }
}

/*
TimestampList1.propTypes = {
  ts: PropTypes.string.isRequired
}
*/


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

    // called after constructor -> render -> native-DOM-magic -> componentDidMount()
    componentDidMount() {
        /*
        See diagram:
        https://projects.wojtekmaj.pl/react-lifecycle-methods-diagram/
        */
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
        /* connects to python websocket server */
        var ws = new WebSocket(ws_address);

        ws.onopen = function() {
            console.log('connected', ws);
        };
        ws.onerror = function(evt) {
            console.error('You need to run a websocket server (that sends data to this webapp): e.g., `python wsock_ejector/wsock_ejector.py`');
            console.log('ws normal error: ', evt, evt.type);  // evt.type is 'error'  typeof evt.type is string
            var moreinfo = evt.target.url;
            console.log("moreinfo", moreinfo);
            document.getElementById("errors-div").innerHTML = "Cannot connect: " + moreinfo;
             //if (ws.readyState == 1) { }
        };


        let that = this;
        ws.onmessage = function (ws_event) {
            // A message received from WebSocket server:
            //console.log("onmessage", ws_event);
            let arrival_time = (new Date())+"";
            let event_content = JSON.parse(ws_event.data);
            //console.log("received event from Queue", ws_event, event_content);
            event_content.timestamps.push(ws_event.timestamp);
            event_content.timestamps.push(arrival_time);

            //console.log(event_content["timestamps"]);  array of strings
            //console.log("ws packet content str", ws_event.data);
            //console.log("ws packet content", event_content);
            // assert
            that.addDrip({
                username: event_content.username,
                amount: event_content.amount,
                timestamps: event_content["timestamps"].map(ts => {return ts;}),
            });

            // failed. how to send something back?
            // ws.send('oggi')
            ws.write('okokok')
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
        //console.log("added drip", new_drip1);
        //this.setState({ drips: [...this.state.chats, data], test: '' });
        var old_drips = this.state.drips;
        var new_drips = old_drips.slice(0); //old_drip.slice(0);
        new_drips.push(new_drip1);
        //this.setState({ drips: new_drips });
        this.setState({drips:new_drips});
        //this.setState({ drips: ["drip A", "drip B"] });
        // this.handleTextChange = this.handleTextChange.bind(this);
        //console.log(this.state);
        //console.log(new_drips);

        // "setState() enqueues changes to the component state and tells React that this component and its children need to be re-rendered with the updated state."
        // "Think of setState() as a request rather than an immediate command to update the component."
        // The update may be defered. It is not immediate.
    }


    render() {
        //<EventBasket timesampsstack='Hello React'></EventBasket>
        //if (this.state.drips.length > 0)
        //    console.log("-----", this.state.drips[0].timestamps+"");
        var k = 0;
        return (
            // shows onlly last 5 items
            // style={"background-color": "#eeeeff";}
            // shadow: https://www.codementor.io/michelre/using-box-shadow-to-construct-a-border-ex0rpxvng
            <div className="ema">
                Recent invoices for <i>{this.props.channel}</i>:
                <ul style={{boxShadow: '3px 3px 5px 6px #ccc', width: '25em'}}>
                    {this.state.drips.slice(-9).map(drip =>
                        // Warning: Each child in an array or iterator should have a unique "key" prop.
                        // <li key={drip.username}>
                        // {drip.timestamps} is converted into string: drip.timestamps+""
                        //span: className="TinyDate"
                        // CSS
                        <li key={++k}><b>£{drip.amount}</b>:
                            {(<TimestampList1 tslist={drip.timestamps}/>)} -- <i>{drip.username}</i> </li>
                            //{drip.timestamps.map(ts=>{return (<TimestampList1 ts={ts}/>)})} -- <i>{drip.username}</i> </li>
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


const dom_element = document.querySelector('#ra-content');
ReactDOM.render(<EventMonitorApp channel="channel-h"/>, dom_element);
console.log("DOM",dom_element);

/*
var messages_dom = document.createElement('ul');
setup_ws("ws://127.0.0.1:5678/", messages_dom);
document.body.appendChild(messages_dom);
*/
console.log("ready.");
