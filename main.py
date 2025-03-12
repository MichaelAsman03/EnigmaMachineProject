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
        self.position = chr(start_position + ord('A'))

    def encode_forward(self, letter):
        index = (ord(letter) - ord('A') + ord(self.position) - ord('A')) % 26
        encoded_letter = self.wiring[index]
        return chr((ord(encoded_letter) - ord(self.position) + ord('A')) % 26 + ord('A'))

    def encode_backward(self, letter):
        index = (ord(letter) - ord('A') + ord(self.position) - ord('A')) % 26
        encoded_letter = chr(self.wiring.index(chr(index + ord('A'))) + ord('A'))
        return chr((ord(encoded_letter) - ord(self.position) + ord('A')) % 26 + ord('A'))

    def rotate(self):
        self.position = chr((ord(self.position) - ord('A') + 1) % 26 + ord('A'))
        return self.position == self.notch
    

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
    def __init__(self, rotors, rotor_positions, plugboard_connections, reflector_type='B'):
        self.rotors = [Rotor(rotors[i], rotor_positions[i]) for i in range(3)]
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
        rotate_next = True
        for rotor in self.rotors:
            if rotate_next:
                rotate_next = rotor.rotate()
            else:
                break

    def encode_message(self, message):
        return ''.join([self.encode_letter(char) for char in message if char.isalpha()])
    
