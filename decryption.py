from main import read_file, encrypt_decrypt, set_random_configs
from collections import Counter
import itertools
from enigma import Rotor, Reflector, Enigma, Keyboard

from operator import itemgetter

rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q", 'I')
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E", 'II')
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V", 'III')
rotor4 = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J", 'IV')
rotor5 = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "Z", 'V')
reflectA = Reflector('EJMZALYXVBWFCRQUONTSPIKHGD')
reflectB = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')
reflectC = Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')
keyboard = Keyboard()

ciphertext = read_file('ciphertext.txt')

print('The message is: ', ciphertext)

print("It's impossible to break it. ")

print('Hint: Try to narrow down the possible combinations')


def index_of_coincidence(text:str) -> float:
    """
    This functions is said to return the index of coincidence of a given text. 
    English texts: ~0.067
    Random texts (like enigma): ~0.038
    Returns: index of coincidence (float) of the given text
    """
    text_clean = [char for char in text.upper() if 'A' <= char <= 'Z']
    frequencies = Counter(text_clean)
    N = len(text_clean)

    # For little texts that are edge cases, we're granting an exception to avoid zero division error

    if N <= 1:
        return 0.0
    
    # Applying the IoC formula

    total_sum = sum([f * (f - 1) for f in frequencies.values()])

    return total_sum / (N * (N - 1))



def test_IoC_rotors(rotor_perm, plainkeys):
    """
    We're testing IOC for each permutation of rotors in every possible key configuration
    It's fairly computable for we'll 5*5*5*26*26*26 ~= 2000000 enigma's configurations
    """

    possible_combinations = []

    sort_key = itemgetter(2)

    Enigmaclass = Enigma
    ioc_func = index_of_coincidence
    encrypt_func = encrypt_decrypt
    keyboard_local = keyboard

    # We'll not search out exhaustively every configuration for rings, reflectors and plugboards. It would grow exponentially.
    # We're using the ioc method to try to find out possible configurations for the rotors

    rotor_left_noused, rotor_mid_noused, rotor_right_noused, rings, keys, reflector, pairs = set_random_configs()
    for perm in rotor_perm:

        enigma_machine = Enigmaclass(pairs, perm[0], perm[1], perm[2], reflector, keyboard_local)
        enigma_machine.set_rings(rings)
    
        for key in plainkeys:    
            # We'll test it for each key
            enigma_machine.set_key(key)
            plaintext = encrypt_func(enigma_machine, ciphertext, rings, key)
            ioc = ioc_func(plaintext)

            possible_combinations.append([[perm[0], perm[1], perm[2]], key, ioc])
            possible_combinations.sort(key=sort_key, reverse=True) #It'll sort according to the ioc
            # To ensure optimisation, we'll set within iteration the top 10 fittest conigurations
            if len(possible_combinations) > 10:
                possible_combinations.pop()
    
    return possible_combinations, reflector, pairs # Only the top 10


def test_ioc_rings(top_combinations, rings_perm, reflector, pairs):

    """
    After testing the main rotors configuration, we can use the ones that yielded the highest index of coincidence.
    We'll use roughly the same logic from the previous function.
    After that we will try to decrypt manually, seeing if the new cipher text (or hopefully the plain one) will be less random.
    """
    possible_combinations = []

    sort_key = itemgetter(3)

    for combination in top_combinations:
        rotor = combination[0]
        key = combination[1]
        enigma_machine = Enigma(pairs, rotor[0], rotor[1], rotor[2], reflector, keyboard)
        enigma_machine.set_key(key)
        for ring in rings_perm:
            enigma_machine.set_rings(ring)
            plaintext = encrypt_decrypt(enigma_machine, ciphertext, ring, key)
            ioc = index_of_coincidence(plaintext)

            possible_combinations.append([[rotor[0], rotor[1], rotor[2]], key, ring, ioc])
            possible_combinations.sort(key=sort_key, reverse=True) #It'll sort according to the ioc
            # To ensure optimisation, we'll set within iteration the top 10 fittest conigurations
            if len(possible_combinations) > 10:
                possible_combinations.pop()

    return possible_combinations



if __name__ == '__main__':

    # debugging
    rotors_permutation = list(itertools.permutations([rotor1, rotor2, rotor3, rotor4, rotor5], 3))
    keys_product = list(itertools.product(range(65, 91), repeat=3))
    rings_product = list(itertools.product(range(1, 27), repeat=2))

    plain_keys = [''.join(map(chr, key)) for key in keys_product]

    top_permutations, reflector, pairs = test_IoC_rotors(rotors_permutation, plain_keys)

    for top in top_permutations:
       print(top[0][0].id, top[0][1].id, top[0][2].id, top[1], top[2])

    # top 3 I V III, V IV III, IV I V

    rings = [(0, ) + ring for ring in rings_product]

    top_permutation = test_ioc_rings(top_permutations, rings, reflector, pairs)

    for top in top_permutation:
      print(top[2])

    #rotor_left_noused, rotor_mid_noused, rotor_right_noused, rings_no_used, keys, reflector, pairs = set_random_configs()

    best_config = top_permutation[0]
    rotor_left = best_config[0][0]
    rotor_mid = best_config[0][1]
    rotor_right = best_config[0][2]
    ring = best_config[2]
    key = best_config[1]
    ioc = best_config[3]

    print(rotor_left.id)
    print(rotor_mid.id)
    print(rotor_right.id)
    print(key)
    print(ring)
    print(ioc)

    rotor_left_noused, rotor_mid_noused, rotor_right_noused, rings_no_used, keys, reflector, pairs = set_random_configs()
    machine = Enigma(pairs, rotor_left, rotor_mid, rotor_right, reflector, keyboard)
    plain_text = encrypt_decrypt(machine, ciphertext, ring, key)

    print(plain_text[:200])

    print(index_of_coincidence(plain_text))
