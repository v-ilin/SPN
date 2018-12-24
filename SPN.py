import numpy as np

table_of_replacement = {
    '000': 0,
    '001': 3,
    '010': 6,
    '011': 5,
    '100': 7,
    '101': 2,
    '110': 4,
    '111': 1
}

backward_table_of_replacement = {
    '000': 0,
    '001': 7,
    '010': 5,
    '011': 1,
    '100': 6,
    '101': 3,
    '110': 2,
    '111': 4
}

binaries = [
    '000',
    '001',
    '010',
    '011',
    '100',
    '101',
    '110',
    '111'
]


def xor(a, b):
    return int(bool(a) != bool(b))


def array_to_string(array):
    string_value = str(array)

    string_value = string_value.replace('[', '')
    string_value = string_value.replace(']', '')
    string_value = string_value.replace(',', '')
    string_value = string_value.replace(' ', '')

    return string_value


def xor_blocks_with_keys(data_blocks, key_blocks):
    result_blocks = []
    for block_index, input_block in enumerate(data_blocks):
        result_block = []
        for i in range(3):
            result = xor(input_block[i], key_blocks[block_index][i])
            result_block.append(result)

        result_blocks.append(result_block)

    return np.array(result_blocks)


def replace_blocks(input_blocks, is_backward):
    replaced_input = []
    for input_block in input_blocks:
        replacement_key = array_to_string(input_block)
        if is_backward:
            index_to_replace = backward_table_of_replacement[replacement_key]
        else:
            index_to_replace = table_of_replacement[replacement_key]

        replaced_block = binaries[index_to_replace]

        replaced_block = np.array(list(replaced_block), dtype=np.int)
        replaced_input.append(replaced_block)

    return np.array(replaced_input)


def mix_elements(blocks):
    result = np.empty(blocks.shape, dtype=np.int)

    result[0][0] = blocks[0][0]
    result[0][1] = blocks[1][0]
    result[0][2] = blocks[2][0]
    result[1][0] = blocks[0][1]
    result[1][1] = blocks[1][1]
    result[1][2] = blocks[2][1]
    result[2][0] = blocks[0][2]
    result[2][1] = blocks[1][2]
    result[2][2] = blocks[2][2]

    return result


def do_round(input_blocks, key_blocks, is_final):
    cripted_input_blocks = xor_blocks_with_keys(input_blocks, key_blocks)
    replaced_blocks = replace_blocks(cripted_input_blocks, False)

    result = replaced_blocks
    # print('cripted_input_blocks = {}'.format(cripted_input_blocks))
    # print('replaced_blocks = {}'.format(replaced_blocks))

    if not is_final:
        result = mix_elements(replaced_blocks)
        # print('mixed_elements = {}'.format(result))
    else:
        result = xor_blocks_with_keys(result, key_blocks)

    return result


def do_1_back_round(input_blocks, key_blocks):
    cripted_input_blocks = xor_blocks_with_keys(input_blocks, key_blocks)
    replaced_blocks = replace_blocks(cripted_input_blocks, True)
    result = xor_blocks_with_keys(replaced_blocks, key_blocks)

    return result


def do_back_round(input_blocks, key_blocks):
    mixed_blocks = mix_elements(input_blocks)
    replaced_blocks = replace_blocks(mixed_blocks, True)
    result = xor_blocks_with_keys(replaced_blocks, key_blocks)

    return result


def calculate_keys_equations(input_text, encrypted_text):
    x = input_text
    y = encrypted_text

    x7y8y9 = xor(x[6], xor(y[7], y[8]))
    x7y5y6 = xor(x[6], xor(y[4], y[5]))
    x7y2y3y8y9 = xor(x[6], xor(xor(y[1], y[2]), xor(y[7], y[8])))
    x7y2y3y5y6 = xor(x[6], xor(xor(y[1], y[2]), xor(y[4], y[5])))

    return [x7y8y9, x7y5y6, x7y2y3y8y9, x7y2y3y5y6]


def encrypt(input_text, key_blocks):
    input_blocks = np.split(input_text, 3)

    blocks_1_round = do_round(input_blocks, key_blocks, False)
    blocks_2_round = do_round(blocks_1_round, key_blocks, False)
    encrypted = do_round(blocks_2_round, key_blocks, True)

    return encrypted


def decrypt(data_encrypted, key_blocks):
    intermediate_result = do_1_back_round(data_encrypted, key_blocks)
    intermediate_result = do_back_round(intermediate_result, key_blocks)
    data_decrypted = do_back_round(intermediate_result, key_blocks)

    return data_decrypted


def main():
    key = np.random.randint(2, size=9)
    key_blocks = np.split(key, 3)

    print('key_blocks = {}'.format(key_blocks))

    input_texts = np.random.randint(2, size=(100, 9))

    keys_equations = []
    for input_text in input_texts:
        data_encrypted = encrypt(input_text, key_blocks).flatten()
        # data_decrypted = decrypt(data_encrypted, key_blocks)

        keys_equation = calculate_keys_equations(input_text, data_encrypted)

        keys_equations.append(keys_equation)

    result = np.sum(keys_equations, axis=0)

    # print('input  = {}'.format(input_text))
    # print('encrypted = {}'.format(data_encrypted))
    # print('decrypted = {}'.format(data_decrypted))
    print('keys_equations = {}'.format(len(keys_equations)))
    print('1 in x7+y8+y9 = {}'.format(result[0]))
    print('1 in x7+y5+y6 = {}'.format(result[1]))
    print('1 in x7+y2+y3+y8+y9 = {}'.format(result[2]))
    print('1 in x7+y2+y3+y5+y6 = {}'.format(result[3]))
    # print('result = {}'.format(result))


if __name__ == '__main__':
    main()