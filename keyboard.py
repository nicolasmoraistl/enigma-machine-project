# The main idea for the keyboard
import enigma

class Keyboard:

    def finding_signal(self, letter):
        """
        This function will find a signal from a letter
    
        Return: (int) the signal
        """

        return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.find(letter.upper())
    
    def finding_letter(self, signal):

        return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[signal]
    

k = Keyboard()

print(k.finding_signal('a'))
