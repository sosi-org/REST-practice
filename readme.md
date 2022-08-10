## Flask / REST practice

CircleCI Badge [![CircleCI](https://circleci.com/gh/sosi-org/REST-practice.svg?style=svg)](https://circleci.com/gh/sosi-org/REST-practice)


## How to
### Setup-I

React <-- WebSocket

STEPS: [1]
#### Step 1
```bash
bash ./scripts/run_setup.bash
```
Then:
```bash
source ./temp/p3-for-me/bin/activate
# python ./app.py &
python ./app.py 1>/dev/ttys000 2>/dev/ttys000 &
```
#### Step 2
Then:
```bash
cd webapp
npm i
mkdir -p public
npm run build  # in webapp/build
npm run watch 1>/dev/ttys000 2>/dev/ttys000 &
```
(tested on node v16.15.0)
See [2]

#### Step 3
Then:
```
python wsock_ejector/wsock_ejector.py
```

#### Step 4
Then:
* Navigate to `file://`....`/REST-practice/webapp/webapp.html` using `open webapp/webapp.html`
or
```bash
python -m SimpleHTTPServer 8080`
open http://127.0.0.1:8000/webapp.html
```

#### Setup 1:
Processes:
1. `python ./app.py`
2. ` `
3. `bash curl_tests.sh`
4. `python wsock_ejector/wsock_ejector.py`

```
wsock_ejector ---ws--->  react app (browser)
```

## References:
[1]  https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
[2] [krasimir/react-bare-minimum](https://github.com/krasimir/react-bare-minimum) and related [post](https://krasimirtsonev.com/blog/article/The-bare-minimum-to-work-with-React) ...


## Featured
* REST
* Flask
* Continuous Integration: circleCI (github)

## Featured (porovisional)
* async [TODO]
* Continuous Integration: circleCI (local) [TODO]
* WebSockets [TODO]
* WSGI

### Some day:
* Secure WebSockets [TODO]

## Terms
* WebSocket Infolets
* Droplet
* channel-h

* Processes:
   * App
   * WebApp (and its server)
   * test (curl)
   * test (python)

## Change log:
* Version 1: As it was on 25 sept 2018 before LBG - [branch: pre-lbg-as-of-25-sep-2018](https://github.com/sosi-org/REST-practice/tree/pre-lbg-as-of-25-sep-2018)
