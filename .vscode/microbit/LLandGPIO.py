def on_forever():
#   basic.show_number(input.light_level())
    if input.light_level() < 5:
        pins.digital_write_pin(DigitalPin.P2,1)
    else:
        pins.digital_write_pin(DigitalPin.P2,0)
    basic.pause(3000)
basic.forever(on_forever)