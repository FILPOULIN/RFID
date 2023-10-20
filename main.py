from pirc522 import RFID
import signal
import time

import RPi.GPIO as GPIO

rdr = RFID()

def is_a_trailer(data):
    return data and data == [0x00] * 16

def somecode():

    GPIO.setup(33, GPIO.OUT)
    data_to_write = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    new_key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x07, 0x80, 0x69, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

    try:
        while True:
            rdr.wait_for_tag()
            (error, tag_type) = rdr.request()
            if not error:
                print("Tag detected")
                (error, uid) = rdr.anticoll()
                if not error:
                    print("UID: " + str(uid))
                    # Select Tag is required before Auth
                    if not rdr.select_tag(uid):
                        # Auth for block 10 (block 2 of sector 2) using default shipping key A
                        if not rdr.card_auth(rdr.auth_b, 9, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
                            # This will print something like (False, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                            if not is_a_trailer(rdr.read(9)):
                                print("Reading block 10: " + str(rdr.read(9)))
                                rdr.write(9, data_to_write)
                                print("Reading block 10: " + str(rdr.read(9)))
                                if not rdr.card_auth(rdr.auth_b, 11, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
                                    print("Reading block 12: " + str(rdr.read(11)))
                                    rdr.write(11, new_key)
                                    print("Reading block 12: " + str(rdr.read(11)))
                                GPIO.output(33, GPIO.HIGH)
                                time.sleep(0.4)
                                GPIO.output(33, GPIO.LOW)
                            # Always stop crypto1 when done working
                            rdr.stop_crypto()
            time.sleep(1)

    except KeyboardInterrupt:
        # Calls GPIO cleanup
        rdr.cleanup()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    somecode()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
