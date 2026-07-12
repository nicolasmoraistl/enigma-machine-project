# Rotors configurations
from enigma import Rotor, Plugboard, Keyboard, Reflector, Enigma


# There are many configurations avaiable in https://en.wikipedia.org/wiki/Enigma_rotor_details

# For the enigma configuration, I've chose the german standard model.

rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q", 12)
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "F", 12)
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "W", 12)
rotor4 = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "K", 12)
rotor5 = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "A", 12)
reflectA = Reflector('EJMZALYXVBWFCRQUONTSPIKHGD')
reflectB = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')
reflectC = Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')
PB = Plugboard(['AR', 'GK', 'OX'])
KB = Keyboard()
"""
# We've "typed" a letter
letter = 'G'

# Enigma doesn't read anything, only electric signal.
signal = KB.finding_signal(letter)

# The enigma workflow for one letter, it's only missing the rotor's rotate  scheme.

signal = PB.forward(signal)

signal = rotor1.forward(signal)

signal = rotor2.forward(signal)

signal = rotor4.forward(signal)

signal = reflectB.reflect(signal)

signal = rotor4.backward(signal)

signal = rotor2.backward(signal)

signal = rotor1.backward(signal)

signal = PB.backward(signal)

letter = KB.finding_letter(signal)


print(letter)
"""


# Rotating mechanism
print(rotor1.left)
print(rotor1.right)

rotor1.rotate_to_letter('G')

print(rotor1.left)
print(rotor1.right)
