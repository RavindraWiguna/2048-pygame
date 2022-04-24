def hex_rgb(hex_str):
    # print(hex_str[0:2])
    # print(hex(hex_str[0:2]))
    r = hex_str[0:2]
    g = hex_str[2:4]
    b = hex_str[4:6]
    print(f'{int(r, 16)},{int(g, 16)},{int(b, 16)}')

while True:
    hex_str = input("color in hex: ")
    hex_rgb(hex_str)
