class Enigma:
    
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ALPHABET_SIZE = 26

class Keyboard(Enigma):

    def finding_signal(self, letter):
        """
        This function will find a signal from a letter
    
        Return: (int) the signal
        """

        return self.ALPHABET.find(letter.upper())
    
    def finding_letter(self, signal):

        return self.ALPHABET[signal]

class Plugboard(Enigma):

    def __init__(self, pairs):
        """
        The data of the class plugboard will receive left and right alphabet. 
        As the plugboard simply converts a letter from one side to another one.
        Pairs will be exactly the pairs of letters from each side of the plugboard.
        """

        self.left = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.right = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

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

class Rotor(Enigma):

    def __init__(self, scramble_config, notch, position = 0):
        """
        The rotor will have initially three arguments.

        scramble_config: a string containing the standard configuration from encryption for each rotor.
        notch: The notch will accuse if the 2nd and the 3rd rotor are to rotate.
        position: The current position of the rotor displayed.
        """
        self.right = scramble_config
        self.left = self.ALPHABET
        self.notch = notch # Is the letter where the Notch is located
        self.position = position
    
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

    def is_notch(self):
        """
        If the position matchs the notch's position, it returns true:

        Returns boolean.
        """

        return self.ALPHABET[self.position] == self.notch
    
    def rotate(self, n=0):
        """
        the left and right sides will each one rotate 1 degree.
        They will be tweaked so the first letter will go to the end.
        """
        for _ in range(n):
            self.left = self.left[1:] + self.left[0]
            self.right = self.right[1:] + self.left[0]

    def rotate_to_letter(self, letter):
        """
        It'll rotate until the letter from the argument becomes the first letter of self.left
        """
        n = self.ALPHABET.find(letter)
        self.rotate(n)

class Reflector(Enigma):

    def __init__(self, scramble_config):

        """
        The reflector is an additional mechanism to improve encryption.
        In the same way as the plugboard, it will change letter by it's pairs.
        Litteraly reflecting 
        """
        self.right = scramble_config

        self.left = self.ALPHABET

    def reflect(self, signal):
        """
        The reflection will get the letter from the right side, the scrambling from the reflector.
        It will receive a new signal.
        It's very similar to the other functions above for it's the same mechanism. It's straighfoward.
        """

        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal

        


        

    


