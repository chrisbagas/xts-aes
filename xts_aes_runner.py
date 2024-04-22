import sys
import binascii

from xts_aes import XTSAES

ENCRYPTION = 'encryption'
DECRYPTION = 'decryption'

TEXT_TYPES = {
    ENCRYPTION: 'plaintext',
    DECRYPTION: 'ciphertext',
}

class XTSAES_RUNNER:
    mode = 'encryption'
    inverse_mode = 'decryption'

    def read_file(self, name, file_path):
        with open(file_path, 'r') as file:
            file_data = file.readlines()[0]
            print('{name}: {data}'.format(name=name, data=file_data))
        return binascii.unhexlify(file_data)
    
    def read_hex_file(self, file_path):
        with open(file_path, 'rb') as file:
            file_data = file.read()

            print('{name} (data): {data}'.format(name=TEXT_TYPES[self.mode], data=file_data))
            if self.mode == ENCRYPTION:
                file_data = self.pad(file_data)

            hex_data = file_data.hex()
            print('{name} (data): {data}'.format(name=TEXT_TYPES[self.mode], data=file_data))
            print('{name} (hex) : {data}'.format(name=TEXT_TYPES[self.mode], data=hex_data))
        hex_data = binascii.unhexlify(hex_data)

        return hex_data
    
    def write_hex_file(self, hex_data, file_type):
        file_path = './output/'
        file_output = 'output.' + file_type
        
        if self.mode == ENCRYPTION:
            file_output += '.txt'
        file_path += file_output
        binary_data = bytes.fromhex(hex_data)

        print('{name} (data): {data}'.format(name=TEXT_TYPES[self.inverse_mode], data=binary_data))
        if self.mode == DECRYPTION:
            binary_data = self.unpad(binary_data)

        with open(file_path, 'wb') as file:
            file.write(binary_data)
            print('{name} (hex) : {data}'.format(name=TEXT_TYPES[self.inverse_mode], data=hex_data))
            print('{name} (data): {data}'.format(name=TEXT_TYPES[self.inverse_mode], data=binary_data))
        return binary_data, file_output

    def read_hex_string(name):
        try:
            hex_string = input('{name}: '.format(name=name))
            hex_string = binascii.unhexlify(hex_string)
        except binascii.Error:
            sys.exit('{name} should be hex string'.format(name=name))

        return hex_string

    def pad(self, str):
        """
        Pad the data using PKCS#7 padding scheme.

        Args:
        - data (bytes): The data to be padded.
        - block_size (int): The block size in bytes.

        Returns:
        - bytes: The padded data.
        """
        block_size = 16
        padding_length = block_size - (len(str) % block_size)
        padding = bytes([padding_length] * padding_length)
        return str + padding
    
    def unpad(self, str): 
        """
        Remove PKCS#7 padding from the data.

        Args:
        - data (bytes): The padded data.

        Returns:
        - bytes: The unpadded data.
        """
        padding_length = str[-1]
        if not (1 <= padding_length <= 16):
            raise ValueError("Invalid padding length")
        return str[:-padding_length]

    def run(self, input_file_path, file_type, key_path):
        # === pre-processing === #
        # key getter
        key = self.read_file('key', key_path)
        if len(key) != 64:
            sys.exit('key should be 64-hex')

        # tweak getter
        tweak_path = './input/.tweak'
        tweak = self.read_file('tweak', tweak_path)
        if len(tweak) != 16:
            sys.exit('tweak should be 16-byte')

        # get file input
        text = self.read_hex_file(input_file_path)

        # === XTSAES processing === #
        xts_aes = XTSAES(key, tweak)

        encryptor = xts_aes.encrypt if self.mode == 'encryption' else xts_aes.decrypt
        ciphertext = encryptor(text)

        result = binascii.hexlify(ciphertext).decode()

        # === post-processing === #
        # write file output
        binary_data, file_output = self.write_hex_file(result, file_type)
        return binary_data, file_output


if __name__ == '__main__':
    xtsaes_runner = XTSAES_RUNNER()

    # file_type = 'txt'
    file_type = input('File type: (txt, png, ...)\n')

    mode = input('Mode: (1: {enc}, 2: {dec})\n'.format(enc=ENCRYPTION, dec=DECRYPTION))
    mode = DECRYPTION if mode == '2' else ENCRYPTION

    if mode  == DECRYPTION:
        xtsaes_runner.mode = 'decryption'
        xtsaes_runner.inverse_mode = 'encryption'

    if xtsaes_runner.mode == ENCRYPTION:
        input_file_path = './input/input.' + file_type
    else:
        input_file_path = './output/output.'+ file_type + '.txt'
    key_path='./input/.key'
    xtsaes_runner.run(input_file_path, file_type,key_path)

# text, image, video, audio, binary executable code