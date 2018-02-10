symbol_pool = [
    '0', '1', '2', '3', '4',
    '5', '6', '7', '8', '9',

    'a', 'b', 'c', 'd', 'e',
    'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y',
    'z',

    'A', 'B', 'C', 'D', 'E',
    'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y',
    'Z'
];
salt_length = 8;

function get_salt() {
    var str = '';
    for (i = 0; i < 8; i++) {
        str += symbol_pool[parseInt(Math.random() * symbol_pool.length, 10)];
    }
    return str;
}