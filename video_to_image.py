import moveipy
import argparse

"""
## video handshake routine
- three items need to be communicated: offset time, dead time, alive time, transmission length
- several full black frames indicates beginning of handshake (1s of continuous frames)
- to transmit a number, we convert it to hex and then 0 postpend to fit the 0xFFFFFF color scheme, then full fill the frame for 1s with it
  - ie. dead time of 8000 is 0x1F40, thus the color to fill the screen with is 0x1F4000
  - do this for dead time and alive time

1s of full screen black (0x000000) 
    -> 1s of full screen dead time color 
    -> 1s of full screen alive time -> 1s of offset time 
    -> 1s transmission length 
    -> wait offset time 
    -> [capture frame in alive window -> wait dead time]*transmission length 
    -> end capture

## video to image stage output
images
- should be of consistent size, but can be of any size
- video is going to strip transparency, but we will still use png format
- no attempt will be made to crop to just information, as such the images may contain extra pixels around border of important info
- images should be named sequentially via numbers (0 indexed), ie. 0.png, 1.png, 2.png... etc

manifest description
- will utilize same duration description, though offset-start may be omitted as it will not be used in processing
    {"duration_desc" : {
        "dead-time-ms": 5000,
        "active-time-ms": 1000
    }}

=======

my inital thoughts are we scan for full black screens and then use a state machine to process the rest,
if we cannot properly parse the information we go to the next all black frame and try again until there
isn't enough video runtime to properly parse the message.

I think for the moment we are going to assume that we are being given video as mp4, but I would like to just
write a wrapper than can take whatever video input and convert it to some constant format, I have a feeling
that moviepy might already do this under the hood so there is potential that we could just abuse that.
"""

def main(argc, argv):
    # https://docs.python.org/3/library/argparse.html#module-argparse
    # https://zulko.github.io/moviepy/
    # https://pillow.readthedocs.io/en/stable/

    pass

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)