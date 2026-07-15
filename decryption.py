from main import read_file, encrypt_decrypt, set_random_configs
from collections import Counter
import itertools
from enigma import Rotor, Reflector, Enigma, Keyboard

rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
rotor4 = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J")
rotor5 = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "Z")
reflectA = Reflector('EJMZALYXVBWFCRQUONTSPIKHGD')
reflectB = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')
reflectC = Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')
keyboard = Keyboard()

ciphertext = read_file('ciphertext.txt')

print('The message is: ', ciphertext)

print("It's impossible to break it. ")

print('Hint: Try to narrow down the possible combinations')


print(ciphertext.replace(' ', ''))

def index_of_coincidence(text:str) -> float:
    """
    This functions is said to return the index of coincidence of a given text. 
    English texts: ~0.067
    Random texts (like enigma): ~0.038
    Returns: index of coincidence (float) of the given text
    """

    frequencies = Counter(text)
    N = len(text)

    # For little texts that are edge cases, we're granting an exception to avoid zero division error

    if N <= 1:
        return 0.0
    
    # Applying the IoC formula

    total_sum = sum([frequencies[letter] * (frequencies[letter] - 1) for letter in frequencies])

    return total_sum / N * (N - 1)

rotors_permutation = list(itertools.permutations([rotor1, rotor2, rotor3, rotor4, rotor5], 3))
keys_permutation = list(itertools.product(range(0, 26), repeat=3))
plain_keys = {''.join(map(chr, key)) for key in keys_permutation}

def test_IoC_rotors(rotor_perm):
    rotor_left, rotor_mid, rotor_right, rings, keys, reflector, pairs = set_random_configs()
    for perm in rotor_perm:
        enigma_machine = Enigma(pairs, perm[0], perm[1], perm[2], reflector, keyboard)
        enigma_machine.set_rings(rings)
    # Wip
