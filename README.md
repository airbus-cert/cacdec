# cacdec
The hidden RDP client recorder

## How does it works ?

cacdec exploit a hidden feature present into The official Microsoft RDP client (aka mstsce.exe). 
RDP is build to use more than one graphical channel. Actually, there is three main channels just for graphical purpose:
* Bitmap directly use by the main channel
* calista codec use into remote fx channel
* H.264 use by dedicated channel

Each of them can produce forensics artefacts. For exemple, ANSSI (a french security agency), built a tools to exploit the bitmap cache used by the main channel, call [bmc-tools](!https://github.com/ANSSI-FR/bmc-tools).


__cacdec__ is a tool to exploit an hidden recoder present into the official RDP client of microsoft, that can dump frames use by the remotefx channel, into bmp format.
This channel is activate when both client and server can use RemoteFX, and the recorder is activable if mstsc version is recent (Windows 10).


## Build cacdec

cacdec use a wrapper around [FreeRDP](!https://github.com/FreeRDP/FreeRDP) to use the calista decoder. This imply to install freerdp from main repository before use __cacdec__

```
sudo apt install cmake zlib1g-dev libglib2.0-dev libssl-dev
```

And then you can install cacdec :

```
python setup.py install
```


## Activate recorder on client machine

To activate recorder set this two registry keys on client
* HKLM\SOFTWARE\Microsoft\Terminal Server Client\EnableRecording DWORD set to one
* HKLM\SOFTWARE\Microsoft\Terminal Server Client\RecordingPath STRING set to output filename

## Parse cacdec stream

```
cacdec -i <input_file> -o /tmp
```
