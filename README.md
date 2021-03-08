# scriptix-io-to-vtt
A small script to convert JSON from Scriptix Speech-to-text real-time API.

I used a modified, by me, version of [scriptix-io/realtime-examples](https://github.com/scriptix-io/realtime-examples) to create a JSON file and needed a way to create a VTT file for VOD use, so I created this small script. It ain't pretty, but it gets the job done.

**Pull requests are welcome.**

## Usage
Show help:

`python to-vtt.py -h`

Convert JSON file to VTT:

`python to-vtt.py captions.json`
