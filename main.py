from datetime import datetime, timedelta

import mido as mido
import pygame


STOP_BUTTONS = {5, 15, 25, 35, 45, 55, 65, 75, 85, 95}
REPEAT_BUTTONS = {6, 16, 26, 36, 46, 66, 66, 76, 86, 96}
RESUME_BUTTONS = {7, 17, 27, 37, 47, 77, 67, 77, 87, 97}


ON = 127

"""
How to install if required
https://wiki.python.org/moin/WindowsCompilers#Microsoft_Visual_C.2B-.2B-_14.2_standalone:_Build_Tools_for_Visual_Studio_2019_.28x86.2C_x64.2C_ARM.2C_ARM64.29
"""
pygame.init()
mido.set_backend("mido.backends.pygame")

if __name__ == '__main__':

    out_names = mido.get_output_names()
    print(out_names)

    # in_port = mido.open_input('HELIX   ')
    # in_port = mido.open_input('USB MIDI Interface')
    # out_port = mido.open_output('loopMIDI Port')

    print("starting")

    # Layer 0
    # pedal 1 = CH 0, PG 0
    # pedal 2 = CH 0, PG 1
    # pedal 3 = CH 0, PG 2
    # ...
    # pedal 10 = CH 0, PG 9

    # Expression A = ch 0, control 27, 1 to 120
    # Expression B = ch 0, control 7, 0 or 127

    # Layer 1
    # pedal 1 = CH 0, PG 10
    # pedal 2 = CH 0, PG 11
    # pedal 3 = CH 0, PG 12
    # ...
    # pedal 10 = CH 0, PG 19

    in_port = mido.open_input('USB MIDI Interface')
    # out_port = mido.open_output('loopMIDI Port')

    last_mode_message = datetime.utcnow() - timedelta(seconds=1)
    MODE_MESSAGE = mido.Message("control_change", channel=0, control=11, value=0, time=0)
    with mido.open_output('loopMIDI Port') as outport:
        with in_port as port:
            for message in port:
                print("receiving message", message)
                if not  hasattr(message, "program"):
                    out_msg =message
                elif message.program in STOP_BUTTONS:
                    out_msg = mido.Message("control_change", channel=0, control=5, value=ON, time=0)
                elif message.program in REPEAT_BUTTONS:
                    out_msg = mido.Message("control_change", channel=0, control=6, value=ON, time=0)
                elif message.program in RESUME_BUTTONS:
                    out_msg = mido.Message("control_change", channel=0, control=7, value=ON, time=0)
                else:
                    out_msg = mido.Message("control_change", channel=0, control=message.program, value=ON, time=0)

                print("sending message to loopMIDI", out_msg)
                outport.send(out_msg
                             )
