import unittest

class Rotor:
    ROTOR_WIRINGS = {
        1: "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        2: "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        3: "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        4: "ESOVPZJAYQUIRHXLNFTGKDCMWB",
        5: "VZBRGITYUPSDNHLXAWMJQOFECK"
    }

    NOTCHES = {
        1: 'Q',
        2: 'E',
        3: 'V',
        4: 'J',
        5: 'Z'
    }

    def __init__(self, rotor_number, start_position):
        self.rotor_number = rotor_number
        self.wiring = self.ROTOR_WIRINGS[rotor_number]
        self.notch = self.NOTCHES[rotor_number]
        self.position = start_position  # Position is now an integer (0-25)

    def encode_forward(self, letter):
        index = (ord(letter) - ord('A') + self.position) % 26
        encoded_letter = self.wiring[index]
        return chr((ord(encoded_letter) - ord('A') - self.position) % 26 + ord('A'))

    def encode_backward(self, letter):
        index = (ord(letter) - ord('A') + self.position) % 26
        encoded_index = self.wiring.index(chr(index + ord('A')))
        return chr((encoded_index - self.position) % 26 + ord('A'))

    def rotate(self):
        self.position = (self.position + 1) % 26
        return self.position == ord(self.notch) - ord('A')


class Plugboard:
    def __init__(self, connections):
        self.wiring = self._create_wiring(connections)

    def _create_wiring(self, connections):
        wiring = {chr(i + ord('A')): chr(i + ord('A')) for i in range(26)}
        for pair in connections:
            if len(pair) == 2:
                wiring[pair[0]] = pair[1]
                wiring[pair[1]] = pair[0]
        return wiring

    def encode(self, letter):
        return self.wiring.get(letter, letter)


class Reflector:
    REFLECTOR_WIRINGS = {
        'A': "EJMZALYXVBWFCRQUONTSPIKHGD",
        'B': "YRUHQSLDPXNGOKMIEBFZCWVJAT",
        'C': "FVPJIAOYEDRZXWGCTKUQSBNMHL"
    }

    def __init__(self, reflector_type):
        self.wiring = self.REFLECTOR_WIRINGS[reflector_type]

    def reflect(self, letter):
        return self.wiring[ord(letter) - ord('A')]


class EnigmaMachine:
    def __init__(self, rotors, rotor_positions, plugboard_connections, reflector_type):
        self.rotors = [Rotor(rotors[i], rotor_positions[i]) for i in range(3)]
        self.initial_positions = rotor_positions  # Save initial positions
        self.plugboard = Plugboard(plugboard_connections)
        self.reflector = Reflector(reflector_type)

    def encode_letter(self, letter):
        letter = self.plugboard.encode(letter)
        for rotor in self.rotors:
            letter = rotor.encode_forward(letter)
        letter = self.reflector.reflect(letter)
        for rotor in reversed(self.rotors):
            letter = rotor.encode_backward(letter)
        letter = self.plugboard.encode(letter)
        self._rotate_rotors()
        return letter

    def _rotate_rotors(self):
        if self.rotors[0].rotate():
            if self.rotors[1].rotate():
                self.rotors[2].rotate()

    def encode_message(self, message):
        return ''.join([self.encode_letter(char) for char in message if char.isalpha()])

    def reset(self):
        """Reset the rotors to their initial positions."""
        for i in range(3):
            self.rotors[i].position = self.initial_positions[i]


class TestRotor(unittest.TestCase):
    def test_encode_forward(self):
        rotor = Rotor(1, 0)  # Rotor I, starting position 0
        self.assertEqual(rotor.encode_forward('A'), 'E')
        self.assertEqual(rotor.encode_forward('B'), 'K')

    def test_encode_backward(self):
        rotor = Rotor(1, 0)  # Rotor I, starting position 0
        self.assertEqual(rotor.encode_backward('E'), 'A')
        self.assertEqual(rotor.encode_backward('K'), 'B')

    def test_rotate(self):
        rotor = Rotor(1, 0)  # Rotor I, starting position 0
        self.assertFalse(rotor.rotate())  # Rotor should not notch at position 0
        self.assertEqual(rotor.position, 1)


class TestPlugboard(unittest.TestCase):
    def test_encode(self):
        plugboard = Plugboard(["AB", "CD"])
        self.assertEqual(plugboard.encode('A'), 'B')
        self.assertEqual(plugboard.encode('B'), 'A')
        self.assertEqual(plugboard.encode('C'), 'D')
        self.assertEqual(plugboard.encode('D'), 'C')
        self.assertEqual(plugboard.encode('E'), 'E')  # Unswapped letter


class TestReflector(unittest.TestCase):
    def test_reflect(self):
        reflector = Reflector('B')
        self.assertEqual(reflector.reflect('A'), 'Y')
        self.assertEqual(reflector.reflect('B'), 'R')


class TestEnigmaMachine(unittest.TestCase):
    def test_encode_message(self):
        rotors = [1, 2, 3]  # Rotor I, II, III
        rotor_positions = [0, 0, 0]  # Starting positions
        plugboard_connections = []  # No plugboard connections
        reflector_type = 'B'  # Reflector B

        enigma = EnigmaMachine(rotors, rotor_positions, plugboard_connections, reflector_type)
        enigma.reset()
        


def main():
    # Predefined settings for simplicity
    rotors = [1, 2, 3]  # Rotor numbers (1-5)
    rotor_positions = [0, 0, 0]  # Starting positions (0-25)
    plugboard_connections = ["AB", "CD", "EF"]  # Plugboard pairs
    reflector_type = 'B'  # Reflector type ('A', 'B', or 'C')

    # Create the Enigma machine
    enigma = EnigmaMachine(rotors, rotor_positions, plugboard_connections, reflector_type)

    while True:
        print("\nCurrent Settings:", "Configured" if enigma else "Not Configured")
        print("Menu:")
        print("1. Configure new Enigma settings")
        print("2. Encrypt a message")
        print("3. Decrypt a message")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nConfigure your Enigma machine settings.")
            rotors = []
            rotor_positions = []
            for i in range(3):
                rotor_num = int(input(f"Enter rotor {i + 1} number (1-5): "))
                rotor_pos = int(input(f"Enter starting position for rotor {i + 1} (0-25): "))
                rotors.append(rotor_num)
                rotor_positions.append(rotor_pos)

            plugboard_pairs = []
            while True:
                pair = input("Enter plugboard pair (2 letters) or 'done' to finish: ").upper()
                if pair == 'DONE':
                    break
                if len(pair) == 2 and pair.isalpha():
                    plugboard_pairs.append(pair)
                else:
                    print("Invalid pair. Please enter exactly 2 letters.")

            enigma = EnigmaMachine(rotors, rotor_positions, plugboard_pairs, reflector_type)
            print("Enigma machine configured successfully.")

        elif choice == '2':
            if enigma:
                message = input("Enter your message: ").upper()
                encrypted_message = enigma.encode_message(message)
                print("Encrypted message:", encrypted_message)
            else:
                print("No settings configured. Please configure settings first.")

        elif choice == '3':
            if enigma:
                enigma.reset()  # Reset the rotors before decrypting
                message = input("Enter your message: ").upper()
                decrypted_message = enigma.encode_message(message)  # Enigma is self-reciprocal
                print("Decrypted message:", decrypted_message)
            else:
                print("No settings configured. Please configure settings first.")

        elif choice == '0':
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    # Run the main program
    main()

    # Run the unit tests
    unittest.main()