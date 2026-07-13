# Rotors configurations
from enigma import Rotor, Plugboard, Keyboard, Reflector, Enigma


# There are many configurations avaiable in https://en.wikipedia.org/wiki/Enigma_rotor_details

# For the enigma configuration, I've chose the german standard model.

rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
rotor4 = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J")
rotor5 = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "Z")
reflectA = Reflector('EJMZALYXVBWFCRQUONTSPIKHGD')
reflectB = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')
reflectC = Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')
plugboard = Plugboard(['CS', 'MF', 'LV'])
keyboard = Keyboard()

def main() -> None:
    # Complete enigma scheme.
    # This first prototype will aim in its logic, a friendly visualization will be afterwards.
    # These configurations can be changed whenever you want.
    enigma_machine = Enigma(plugboard, rotor1, rotor2, rotor3, reflectB, keyboard)

    enigma_machine.set_key('KEY')

    enigma_machine.set_rings((1, 1, 2))

    message = input()

    message = message.upper()

    ciphertext = ''

    for letter in message:
        ciphertext += enigma_machine.encryption_char(letter)


    print(ciphertext)


main()
