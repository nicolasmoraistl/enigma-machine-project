ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Enigma:
    
    def __init__(self, plugboard:Plugboard, left_rotor:Rotor, mid_rotor:Rotor, right_rotor:Rotor, reflector:Reflector, keyboard:Keyboard):

        self.plugboard = plugboard
        self.right_rotor = right_rotor
        self.mid_rotor = mid_rotor
        self.left_rotor = left_rotor
        self.reflector = reflector
        self.keyboard = keyboard
        

    def set_key(self, key):
        self.left_rotor.rotate_to_letter(key[0])
        self.mid_rotor.rotate_to_letter(key[1])
        self.right_rotor.rotate_to_letter(key[2])

    def encryption_char(self, letter):

        """
        The encryption "workflow" for a specific character.
        The rotation is now implemented
        """
        # If blank space, then return it immediately
        if letter == ' ':
            return letter
        # Here is the rotation scheme, the second and the third will rotate if the notch match the current letter.
        # The stardard position for the matching is 0.
        #If the notch is matched in the mid rotor, then both will rotate.
        
        if self.mid_rotor.left[0] == self.mid_rotor.notch:
            self.mid_rotor.rotate()
            self.left_rotor.rotate()
        # If only the right rotor matchs, then only the mid rotor will rotate
        elif self.right_rotor.left[0] == self.right_rotor.notch:
            self.mid_rotor.rotate()

        # This will always rotate
        self.right_rotor.rotate()

        # Character encryption
        signal = self.keyboard.finding_signal(letter)
        signal = self.plugboard.forward(signal)
        signal = self.right_rotor.forward(signal)
        signal = self.mid_rotor.forward(signal)
        signal = self.left_rotor.forward(signal)
        signal = self.reflector.reflect(signal)
        signal = self.left_rotor.backward(signal)
        signal = self.mid_rotor.backward(signal)
        signal = self.right_rotor.backward(signal)
        signal = self.plugboard.backward(signal)
        letter = self.keyboard.finding_letter(signal)
        
        return letter

    def set_rings(self, rings):
        """
        A tuple containing 3 integers for each rotor will represent the rings that will rotate backwardly.
        """
        self.left_rotor.set_ring(rings[0])
        self.mid_rotor.set_ring(rings[1])
        self.right_rotor.set_ring(rings[2])


class Keyboard:

    def finding_signal(self, letter):
        """
        This function will find a signal from a letter
    
        Return: (int) the signal
        """

        return ALPHABET.find(letter.upper())
    
    def finding_letter(self, signal):

        return ALPHABET[signal]

class Plugboard:

    def __init__(self, pairs):
        """
        The data of the class plugboard will receive left and right alphabet. 
        As the plugboard simply converts a letter from one side to another one.
        Pairs will be exactly the pairs of letters from each side of the plugboard.
        """

        self.left = ALPHABET
        self.right = ALPHABET

        for pair in pairs:
            A = pair[0]
            B = pair[1]
            position_A = self.left.find(A)
            position_B = self.left.find(B)
            self.left = self.left[:position_A] + B + self.left[position_A+1:]
            self.left = self.left[:position_B] + A + self.left[position_B+1:]

    def forward(self, signal):
        """
        The right side containing the corresponding plug will be transformed into a new signal
        from the original alphabet position until the left side
        """
        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal

    def backward(self, signal):
        """
        When returning from the reflector, it will pass from the left side, contaning the alphabet,
        to the right side, with the modifications from the plugboard.
        """
        letter = self.left[signal]
        signal = self.right.find(letter)
        return signal

class Rotor:

    def __init__(self, scramble_config, notch):
        """
        The rotor will have initially three arguments.

        scramble_config: a string containing the standard configuration from encryption for each rotor.
        notch: The notch will accuse if the 2nd and the 3rd rotor are to rotate.
        """
        self.right = scramble_config
        self.left = ALPHABET
        self.notch = notch # Is the letter where the Notch is located

    def forward(self, signal):
        """
        The right side containing the scramble configuration will be transformed into a new signal
        from the original alphabet position until the left side
        """
        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal

    def backward(self, signal):
        """
        When returning from the reflector, it will pass from the left side, contaning the alphabet,
        to the scrambled key of the rotor.
        """
        letter = self.left[signal]
        signal = self.right.find(letter)
        return signal
    
    def rotate(self, n=1, forward=True):
        """
        the left and right sides will each one rotate 1 degree.
        They will be tweaked so the first letter will go to the end.
        Forward will guide the direction of the rotation.
        """
        for _ in range(n):
            if forward:
                self.left = self.left[1:] + self.left[0]
                self.right = self.right[1:] + self.right[0]
            else:
                self.left = self.left[25] + self.left[:25]
                self.right = self.right[25] + self.right[:25]


    def rotate_to_letter(self, letter):
        """
        It'll rotate until the letter from the argument becomes the first letter of self.left
        """
        while self.left[0] != letter:
            self.rotate()

    def set_ring(self, n):
        # Each ring will make the rotation moves backward instead of forward.
        
        self.rotate(n - 1, forward=False)
        if n > 1:
            n_notch = ALPHABET.find(self.notch)
            self.notch = ALPHABET[(n_notch - n) % 26]

class Reflector:

    def __init__(self, scramble_config):

        """
        The reflector is an additional mechanism to improve encryption.
        In the same way as the plugboard, it will change letter by it's pairs.
        Litteraly reflecting 
        """
        self.right = scramble_config

        self.left = ALPHABET

    def reflect(self, signal):
        """
        The reflection will get the letter from the right side, the scrambling from the reflector.
        It will receive a new signal.
        It's very similar to the other functions above for it's the same mechanism. It's straighfoward.
        """

        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal

        


        

    


