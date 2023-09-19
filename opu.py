OPU_COM_list = {
    'BigInf': {'MAGIC': b'\xFF',
               'OPU_ID': b'\x01',
               'ZERO': b'\x00',
               'RATIO_DEG': 112,
               'GET_TEMP': b'\x00\x91',
               'QUERY_TEMP': b'$t',  # ???????
               'GET_POS': b'\x00\x51',
               'QUERY_POS': b'\x00\x59',
               'SET_POS': b'\x00\x71',
               },
    'TL.0100': {'MAGIC': b'\xFF',
                'OPU_ID': b'\x01',
                'ZERO': b'\x00',
                'RATIO_DEG': 100,
                'GET_TEMP': b'$t#',
                'QUERY_TEMP': b'$t',
                'GET_POS': b'\x00\x51',
                'QUERY_POS': b'\x00\x59',
                'SET_POS': b'\x00\x4b',
                },
}


class OPU():
    MAGIC = None
    OPU_ID = None
    ZERO = None
    RATIO_DEG = None
    GET_TEMP = None
    QUERY_TEMP = None
    SET_POS = None
    GET_POS = None
    QUERY_POS = None

    def __init__(self, type_opu) -> None:
        self.type_opu = type_opu

        set = OPU_COM_list[type_opu]
        self.MAGIC = set['MAGIC']
        self.OPU_ID = set['OPU_ID']
        self.ZERO = set['ZERO']
        self.RATIO_DEG = set['RATIO_DEG']
        self.GET_TEMP = set['GET_TEMP']
        self.QUERY_TEMP = set['QUERY_TEMP']
        self.SET_POS = set['SET_POS']
        self.GET_POS = set['GET_POS']
        self.QUERY_POS = set['QUERY_POS']

    def get_temp(self) -> bytes:
        if self.type_opu == 'BigInf':
            comm = self.__gen_bytes(self.GET_TEMP, 2*self.ZERO)
        if self.type_opu == "TL.0100":
            comm = self.GET_TEMP
        return comm

    def get_pos_pan(self) -> bytes:
        comm = self.__gen_bytes(self.GET_POS, 2*self.ZERO)
        return comm

    def set_pos_pan(self, deg: int) -> bytes:
        deg_bytes = self.conv_deg_b(deg)
        return self.__gen_bytes(self.SET_POS, deg_bytes)

    def conv_deg_b(self, deg) -> bytes:
        deg = deg*self.RATIO_DEG
        return bytes([deg//256, deg % 256])

    def __gen_bytes(self, *command) -> bytes:
        string_b = self.OPU_ID
        for com in command:
            string_b += com
        return self.MAGIC + string_b + bytes([sum(string_b) % 256])

    def conv_b_deg(self, str_bytes) -> float:
        deg_HH = str_bytes[4]
        deg_LL = str_bytes[5]
        deg = (deg_HH*256 + deg_LL) / 100
        return deg
    
    def verification(self, response, query):
        pass


if __name__ == '__main__':
    type_opu = 'TL.0100'

    opu = OPU(type_opu)
    temp = opu.get_temp()
    print(f"Температура ОПУ: {temp}")
    pos = opu.get_pos_pan()
    print(f"Положение ОПУ (Азимут): {pos}")
    deg = 30
    print(f'Меняем угол на {deg}')
    pos = opu.set_pos_pan(deg)
    print(f"Положение ОПУ (Азимут): {pos}")
