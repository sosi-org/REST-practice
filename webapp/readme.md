To install:
```
npm i
npm run build
npm run watch &
```
Load the `webapp.html` on browser and then run the server
```
python wsock_ejector.py
```

The packets of data (here "Drips", containing `Invoice`s) sent by the WebSockets server (on Python) are received by the browser and displayed using React. The timestamps are shown to measure and profile the latency throughout the stack:

Data Flow:

(Queue &rarr; →)
Python (fetch from queue) &rarr;
WebSocket (server) &rarr;
Websocket (browser; via `onmessage()`) &rarr;
React (state; via `setState()`) &rarr;
React JSX `render()`.

(The Queue is to be implemented.

See also:
[1] https://github.com/krasimir/react-bare-minimum
