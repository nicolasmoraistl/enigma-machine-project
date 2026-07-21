# Rotors configurations
from enigma import Rotor, Plugboard, Keyboard, Reflector, Enigma
import random

# There are many configurations avaiable in https://en.wikipedia.org/wiki/Enigma_rotor_details

# For the enigma configuration, I've chose the german standard model.

rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q", 'I')
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E", 'II')
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V", 'III')
rotor4 = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J", 'IV')
rotor5 = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "Z", 'V')
reflectA = Reflector('EJMZALYXVBWFCRQUONTSPIKHGD')
reflectB = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')
reflectC = Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')
keyboard = Keyboard()


def read_file(file):

    with open(file, 'r', encoding='utf-8') as file:
        content = file.read()
        return content

def create_file(text:str):

    with open('ciphertext.txt', 'w', encoding='utf-8') as file:
        file.write(text)

def encrypt_decrypt(machine:Enigma, message:str, rings, keys):

    machine.set_rings(rings)

    machine.set_key(keys)

    enigma_text = ''

    enigma_text = ''.join([machine.encryption_char(letter) for letter in message])

    return enigma_text


def set_random_configs() -> tuple:

    rotors = [rotor1, rotor2, rotor3, rotor4, rotor5]
    machine_rotors = []

    for _ in range(3):
        rotor = random.choice(rotors)
        rotors.remove(rotor)
        machine_rotors.append(rotor)

    rotor_left = machine_rotors[0]
    rotor_mid = machine_rotors[1]
    rotor_right = machine_rotors[2]

    rings = []

    for _ in range(3):
        rings.append(random.randint(1, 26))

    rings = tuple(rings)

    keys = ''
    for _ in range(3):
        n_ascii = random.randint(65, 90)
        keys += chr(n_ascii)
        
    reflectors = [reflectA, reflectB, reflectC]
    reflector = random.choice(reflectors)

    n_pairs = random.randint(1, 13)

    avaiable = list(range(65, 91))
    
    pairs = []

    for _ in range(n_pairs):

    
        pair1 = random.choice(avaiable)
        avaiable.remove(pair1)
        pair2 = random.choice(avaiable)
        avaiable.remove(pair2)
    
        pair = chr(pair1) + chr(pair2)
        pairs.append(pair)
    plugboard = Plugboard(pairs)

    return (rotor_left, rotor_mid, rotor_right, rings, keys, reflector, plugboard)



    

def main() -> None:
    # Complete enigma scheme.
    # This first prototype will aim in its logic, a friendly visualization will be afterwards.
    # These configurations can be changed whenever you want.
    rotor_left, rotor_mid, rotor_right, rings, keys, reflector, pairs = set_random_configs()

    enigma_machine = Enigma(pairs, rotor_left, rotor_mid, rotor_right, reflector, keyboard)

    message = read_file('message.txt')

    ciphertext = encrypt_decrypt(enigma_machine, message, rings, keys)
    
    create_file(ciphertext)


if __name__ == '__main__':
    main()