# cacdec
The hidden mstsc recorder player

## Activate recorder

To activate recorder set this two registry keys on client
* HKLM\SOFTWARE\Microsoft\Terminal Server Client\EnableRecording set to one
* HKLM\SOFTWARE\Microsoft\Terminal Server Client\RecordingPath set to output folder

## Build cacdec

```
python setup.py install
```

## Parse cacdec stream

```
cacdec -i <input_file> -o /tmp
```
