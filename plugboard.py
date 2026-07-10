import enigma

class Plugboard:

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

p = Plugboard(["AF", "CR"])

print(p.left)
print(p.right)



