from datetime import datetime, timedelta

import mido as mido

if __name__ == '__main__':
    out_names = mido.get_output_names()
    print(out_names)

    # in_port = mido.open_input('HELIX   ')
    in_port = mido.open_input('USB MIDI Interface')
    out_port = mido.open_output('PY OUT', virtual=True, client_name='PY OUT')

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

    last_mode_message = datetime.utcnow() - timedelta(seconds=1)
    MODE_MESSAGE = mido.Message("control_change", channel=0, control=11, value=0, time=0)
    with mido.open_output('PY OUT', virtual=True, client_name='PY OUT') as outport:
        with in_port as port:
            for message in port:
                print("receiving message", message)
                print("sending message to PY OUT", message)
                outport.send(message)
