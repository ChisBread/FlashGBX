#coding:utf8

#libbacon.so binding

# int spi_init(const char *user_path, uint32_t user_speed, bool verbose);
# void spi_close();
# void reset_chip();
# int power_control(bool v3_3v, bool v5v);
# int read_power();
# int agb_read_cart_30bit(char **keys, uint32_t *values, size_t size);
# void agb_read_rom(uint32_t addr, uint32_t size, bool hwaddr, bool reset, uint8_t *rx_buffer);
# void agb_write_rom_sequential(uint32_t addr, const uint16_t *data, size_t size, bool hwaddr, bool reset);
# void agb_write_rom_sequential_bytes(uint32_t addr, const uint8_t *data, size_t size, bool hwaddr, bool reset);
# void agb_write_rom_with_address(uint32_t *addrs, uint16_t *datas, size_t size, bool hwaddr, bool reset);
# void agb_read_ram(uint16_t addr, uint32_t size, bool reset, uint8_t *rx_buffer);
# void agb_write_ram(uint16_t addr, const uint8_t *data, size_t size, bool reset);
# void agb_write_ram_with_address(uint16_t *addrs, uint8_t *datas, size_t size, bool reset);
# void clear_pipeline();
# void execute_pipeline();
# void agb_write_rom_sequential_pipeline(uint32_t addr, const uint16_t *data, size_t size, bool hwaddr, bool reset);
# void agb_write_rom_sequential_bytes_pipeline(uint32_t addr, const uint8_t *data, size_t size, bool hwaddr, bool reset);
# void agb_write_rom_with_address_pipeline(uint32_t *addrs, uint16_t *datas, size_t size, bool hwaddr, bool reset);
# void agb_write_ram_with_address_pipeline(uint16_t *addrs, uint8_t *datas, size_t size, bool reset);
### handler
# struct pipeline_handler;
# pipeline_handler* new_pipeline_handler();
# void free_pipeline_handler(pipeline_handler *handler);
# void execute_pipeline_with_handler(pipeline_handler *handler, size_t idx);
# pipeline_handler* agb_write_rom_sequential_bytes_pipeline_with_handler(uint32_t addr, const uint8_t *data, size_t size, bool hwaddr, bool reset, pipeline_handler *handler);
# pipeline_handler* agb_write_rom_with_address_pipeline_with_handler(uint32_t *addrs, uint16_t *datas, size_t size, bool hwaddr, bool reset, pipeline_handler *handler);

import ctypes
import os
import sys
import time

ROM_MAX_SIZE = 0x2000000
RAM_MAX_SIZE = 0x20000
RAM_512_SIZE = 0x10000

class BaconWritePipeline:
    def __init__(self, flush_func):
        self.flush_func = flush_func
    def Flush(self):
        self.flush_func()
        return self

class Bacon:
    def __init__(self, libbacon=None, auto_connect=True):
        if libbacon is None:
            find_list = [os.path.join(os.path.dirname(__file__), "libbacon.so"), os.path.join(os.path.dirname(__file__), "build/libbacon.so"), "/usr/local/lib/libbacon.so", "/usr/lib/libbacon.so"]
            for libbacon_path in find_list:
                if os.path.exists(libbacon_path):
                    self.libbacon = ctypes.CDLL(libbacon_path)
                    break
            else:
                print("libbacon.so not found.")
                sys.exit(1)
        else:
            self.libbacon = ctypes.CDLL(libbacon)
        self.libbacon.spi_init.argtypes = [ctypes.c_char_p, ctypes.c_uint32, ctypes.c_ubyte]
        self.libbacon.spi_init.restype = ctypes.c_int
        self.libbacon.spi_close.argtypes = []
        self.libbacon.spi_close.restype = None
        self.libbacon.reset_chip.argtypes = []
        self.libbacon.reset_chip.restype = None
        self.libbacon.power_control.argtypes = [ctypes.c_bool, ctypes.c_bool]
        self.libbacon.power_control.restype = ctypes.c_int
        self.libbacon.read_power.argtypes = []
        self.libbacon.read_power.restype = ctypes.c_int
        self.libbacon.agb_read_cart_30bit.argtypes = [ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_uint32), ctypes.c_size_t]
        self.libbacon.agb_read_cart_30bit.restype = ctypes.c_int
        self.libbacon.agb_read_rom.argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_bool, ctypes.c_bool, ctypes.POINTER(ctypes.c_uint8)]
        self.libbacon.agb_read_rom.restype = None
        self.libbacon.agb_write_rom_sequential.argtypes = [ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint16), ctypes.c_size_t, ctypes.c_bool, ctypes.c_bool]
        self.libbacon.agb_write_rom_sequential.restype = None
        self.libbacon.agb_write_rom_sequential_bytes.argtypes = [ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.c_bool, ctypes.c_bool]
        self.libbacon.agb_write_rom_sequential_bytes.restype = None
        self.libbacon.agb_write_rom_with_address.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint16), ctypes.c_size_t, ctypes.c_bool, ctypes.c_bool]
        self.libbacon.agb_write_rom_with_address.restype = None
        self.libbacon.agb_read_ram.argtypes = [ctypes.c_uint16, ctypes.c_uint32, ctypes.c_bool, ctypes.POINTER(ctypes.c_uint8)]
        self.libbacon.agb_read_ram.restype = None
        self.libbacon.agb_write_ram.argtypes = [ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.c_bool]
        self.libbacon.agb_write_ram.restype = None
        self.libbacon.agb_write_ram_with_address.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.c_bool]
        self.libbacon.agb_write_ram_with_address.restype = None

        self.libbacon.clear_pipeline.argtypes = []
        self.libbacon.clear_pipeline.restype = None
        self.libbacon.execute_pipeline.argtypes = []
        self.libbacon.execute_pipeline.restype = None
        self.libbacon.agb_write_rom_sequential_pipeline.argtypes = [ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint16), ctypes.c_size_t, ctypes.c_bool, ctypes.c_bool]
        self.libbacon.agb_write_rom_sequential_pipeline.restype = None
        self.libbacon.agb_write_rom_sequential_bytes_pipeline.argtypes = [ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.c_bool, ctypes.c_bool]
        self.libbacon.agb_write_rom_with_address_pipeline.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint16), ctypes.c_size_t, ctypes.c_bool, ctypes.c_bool]
        self.libbacon.agb_write_rom_with_address_pipeline.restype = None
        self.libbacon.agb_write_ram_with_address_pipeline.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.c_bool]
        self.libbacon.agb_write_ram_with_address_pipeline.restype = None

        self.libbacon.new_pipeline_handler.argtypes = []
        self.libbacon.new_pipeline_handler.restype = ctypes.c_void_p
        self.libbacon.free_pipeline_handler.argtypes = [ctypes.c_void_p]
        self.libbacon.free_pipeline_handler.restype = None
        self.libbacon.execute_pipeline_with_handler.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
        self.libbacon.execute_pipeline_with_handler.restype = None
        self.libbacon.agb_write_rom_sequential_bytes_pipeline_with_handler.argtypes = [ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.c_bool, ctypes.c_bool, ctypes.c_void_p]
        self.libbacon.agb_write_rom_sequential_bytes_pipeline_with_handler.restype = ctypes.c_void_p
        self.libbacon.agb_write_rom_with_address_pipeline_with_handler.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint16), ctypes.c_size_t, ctypes.c_bool, ctypes.c_bool, ctypes.c_void_p]
        self.libbacon.agb_write_rom_with_address_pipeline_with_handler.restype = ctypes.c_void_p


        if auto_connect:
            self.spi_init(b"/dev/spidev3.0", 32000000, False)

        self.power = 0

    def spi_init(self, user_path, user_speed, verbose):
        return self.libbacon.spi_init(user_path, user_speed, verbose)
    
    def spi_close(self):
        return self.libbacon.spi_close()

    def reset_chip(self):
        return self.libbacon.reset_chip()

    def power_control(self, v3_3v, v5v):
        return self.libbacon.power_control(v3_3v, v5v)

    def read_power(self):
        return self.libbacon.read_power()

    def agb_read_cart_30bit(self):
        keys = (ctypes.c_char_p * 30)( *[b"000000000000" for i in range(30)] )
        values = (ctypes.c_uint32 * 30)( *[0 for i in range(30)] )
        size = 30
        ret = self.libbacon.agb_read_cart_30bit(keys, values, size)
        if ret == 0:
            return dict([(key.decode("utf-8"), value) for key, value in zip(keys, values)])
        else:
            return None

    def agb_read_rom(self, addr, size, hwaddr = False, reset = True):
        rx_buffer = (ctypes.c_uint8 * size)()
        self.libbacon.agb_read_rom(addr, size, hwaddr, reset, rx_buffer)
        return rx_buffer

    def agb_write_rom_sequential(self, addr, data: bytes, hwaddr = False, reset = True):
        size = len(data)
        data = (ctypes.c_uint8 * size)(*data)
        self.libbacon.agb_write_rom_sequential_bytes(addr, data, size, hwaddr, reset)

    def agb_write_rom_with_address(self, commands, hwaddr = False, reset = True):
        size = len(commands)
        commands = (
            (ctypes.c_uint32 * size)(*[command[0] for command in commands]),
            (ctypes.c_uint16 * size)(*[command[1] for command in commands])
        )
        self.libbacon.agb_write_rom_with_address(commands[0], commands[1], size, hwaddr, reset)

    def agb_read_ram(self, addr, size, reset = True):
        rx_buffer = (ctypes.c_uint8 * size)()
        self.libbacon.agb_read_ram(addr, size, reset, rx_buffer)
        return rx_buffer

    def agb_write_ram(self, addr, data, size, reset = True):
        data = (ctypes.c_uint8 * size)(*data)
        self.libbacon.agb_write_ram(addr, data, size, reset)

    def clear_pipeline(self):
        return self.libbacon.clear_pipeline()
    
    def execute_pipeline(self):
        return self.libbacon.execute_pipeline()
    
    def agb_write_rom_sequential_pipeline(self, addr, data: bytes, hwaddr = False, reset = True):
        size = len(data)
        data = (ctypes.c_uint8 * size)(*data)
        self.libbacon.agb_write_rom_sequential_bytes_pipeline(addr, data, size, hwaddr, reset)

    def agb_write_rom_with_address_pipeline(self, commands, hwaddr = False, reset = True):
        size = len(commands)
        commands = (
            (ctypes.c_uint32 * size)(*[command[0] for command in commands]),
            (ctypes.c_uint16 * size)(*[command[1] for command in commands])
        )
        self.libbacon.agb_write_rom_with_address_pipeline(commands[0], commands[1], size, hwaddr, reset)

    def agb_write_ram_with_address_pipeline(self, commands, reset = True):
        size = len(commands)
        commands = (
            (ctypes.c_uint16 * size)(*[command[0] for command in commands]),
            (ctypes.c_uint8 * size)(*[command[1] for command in commands])
        )
        self.libbacon.agb_write_ram_with_address_pipeline(commands[0], commands[1], size, reset)

    def new_pipeline_handler(self):
        return self.libbacon.new_pipeline_handler()
    def free_pipeline_handler(self, handler):
        return self.libbacon.free_pipeline_handler(handler)
    def execute_pipeline_with_handler(self, handler, idx=0):
        return self.libbacon.execute_pipeline_with_handler(handler, idx)
    def agb_write_rom_sequential_bytes_pipeline_with_handler(self, handler, addr, data: bytes, hwaddr = False, reset = True):
        size = len(data)
        data = (ctypes.c_uint8 * size)(*data)
        return self.libbacon.agb_write_rom_sequential_bytes_pipeline_with_handler(addr, data, size, hwaddr, reset, handler)
    def agb_write_rom_with_address_pipeline_with_handler(self, handler, commands, hwaddr = False, reset = True):
        size = len(commands)
        commands = (
            (ctypes.c_uint32 * size)(*[command[0] for command in commands]),
            (ctypes.c_uint16 * size)(*[command[1] for command in commands])
        )
        return self.libbacon.agb_write_rom_with_address_pipeline_with_handler(commands[0], commands[1], size, hwaddr, reset, handler)

    ################# 兼容FlashGBX的接口 #################
    def Close(self):
        self.spi_close()
    def ResetChip(self) -> BaconWritePipeline:
        self.reset_chip()
        return BaconWritePipeline(self.execute_pipeline)
    def PowerControl(self, v3_3v, v5v):
        if v3_3v:
            self.power = 3
        elif v5v:
            self.power = 5
        else:
            self.power = 0
        self.power_control(v3_3v, v5v)
        return BaconWritePipeline(self.execute_pipeline)
    def AGBReadROM(self, addr: int, size: int, reset=True, callback=None) -> bytes:
        ret = bytes(self.agb_read_rom(addr, size, False, reset))
        return ret
    def ResetChip(self) -> BaconWritePipeline:
        self.reset_chip()
        return BaconWritePipeline(self.execute_pipeline)
    def AGBWriteROMSequential(self, addr, data: bytes, reset=True, callback=None) -> BaconWritePipeline:
        self.agb_write_rom_sequential_pipeline(addr, data, False, reset)
        return BaconWritePipeline(self.execute_pipeline)
    def AGBWriteROMWithAddress(self, commands: list, callback=None) -> BaconWritePipeline:
        self.agb_write_rom_with_address_pipeline(commands, False)
        return BaconWritePipeline(self.execute_pipeline)
    def AGBReadRAM(self, addr: int, size: int, bankswitch=None, callback=None) -> bytes:
        ret = bytes(self.agb_read_ram(addr, size))
        return ret
    
    def AGBWriteRAM(self, addr: int, data: bytes, bankswitch=None, callback=None) -> bool:
        self.agb_write_ram(addr, data, len(data), True)
        return True
    def AGBWriteRAMWithAddress(self, commands: list, reset=True, callback=None) -> BaconWritePipeline:
        self.agb_write_ram_with_address_pipeline(commands, reset)
        return BaconWritePipeline(self.execute_pipeline)

def test_readrom(bacon):
    readsize = ROM_MAX_SIZE
    start = time.time() * 1000
    rom = bacon.agb_read_rom(0, readsize)
    for i in range(10):
        print("%02x" % rom[i], end="")
    print()
    cost = time.time() * 1000 - start
    print("Read ROM data cost %f seconds, speed: %fKB/s" % (cost/1000.0, readsize / (cost/1000.0) / 1024.0))
def test_readram(bacon):
    readsize = RAM_512_SIZE
    start = time.time() * 1000
    ram = bacon.agb_read_ram(0, readsize)
    for i in range(10):
        print("%02x" % ram[i], end="")
    print()
    cost = time.time() * 1000 - start
    print("Read RAM data cost %f seconds, speed: %fKB/s" % (cost/1000.0, readsize / (cost/1000.0) / 1024.0))
def test_writeram(bacon):
    with open(sys.argv[2], "rb") as f:
        body = f.read()
        print("Clear RAM data")
        bacon.agb_write_ram(0, b"\x00" * len(body), len(body))
        ram = bytes(bacon.agb_read_ram(0, len(body)))
        if ram == b"\x00" * len(body):
            print("Clear RAM data success.")
        else:
            print("Clear RAM data failed.")
        start = time.time() * 1000
        print("Write RAM data: %s" % body[:10].hex())
        bacon.agb_write_ram(0, body, len(body))
        cost = time.time() * 1000 - start
        print("Write RAM data cost %f seconds, speed: %fKB/s" % (cost/1000.0, len(body) / (cost/1000.0) / 1024.0))
        print("Check RAM data")
        ram = bytes(bacon.agb_read_ram(0, len(body)))
        print("Read RAM data: %s" % bytes(ram)[:10].hex())
        if ram == body:
            print("Check RAM data success.")
        else:
            print("Check RAM data failed.")
def read_flashid(bacon):
    flashid = bytes(bacon.agb_read_rom(0, 4))
    print("Data 0-3: %s" % flashid.hex())
    bacon.agb_write_rom_with_address_pipeline([
        [0xAAA, 0xAA],
        [0x555, 0x55],
        [0xAAA, 0x90]
    ])
    bacon.execute_pipeline()
    flashid = bytes(bacon.agb_read_rom(0, 4))
    print("Flash ID: %s" % flashid.hex())
    # reset
    bacon.agb_write_rom_with_address_pipeline([[0, 0xF0]])
    bacon.execute_pipeline()
    return flashid
def rewrite_first_sector(bacon, addr=0):
    ret = bytes(bacon.agb_read_rom(addr, 0x20000))
    print("Data", ret[:10].hex())
    bacon.agb_write_rom_with_address_pipeline([
        [0xAAA, 0xAA],
        [0x555, 0x55],
        [0xAAA, 0x80],
        [0xAAA, 0xAA],
        [0x555, 0x55],
        [addr, 0x30]
    ])
    bacon.execute_pipeline()
    while True:
        ret = bytes(bacon.agb_read_rom(addr, 0x20000))
        if ret == b"\xFF" * 0x20000:
            break
        print("Sector erase wait.", ret[:10].hex())
        time.sleep(0.1)
    print("Sector erase success.")
    flash_buffer_write = [
        [0xAAA, 0xAA],
        [0x555, 0x55],
        [addr, 0x25],
        [addr, 0xFF],
    ]
    flash_buffer_write_commit = [
        [addr, 0x29]
    ]
    for i in range(0, 0x20000, 0x200): # buffer 512byte
        bacon.agb_write_rom_with_address_pipeline(flash_buffer_write, False, True)
        bacon.agb_write_rom_sequential_pipeline(addr + i, b"\x00" * 0x200, False, False)
        bacon.agb_write_rom_with_address_pipeline(flash_buffer_write_commit, False, True)
        bacon.execute_pipeline()
        ret = bytes(bacon.agb_read_rom(addr + i,0x200))
        retry = 0
        while ret != b"\x00" * 0x200:
            print("Write wait.", ret[:10].hex())
            time.sleep(0.1)
            if retry > 100:
                print("Write failed.")
                return
            retry += 1
        print("Write success.")
if __name__ == "__main__":
    bacon = Bacon()
    bacon.power_control(True, False) # 3.3V
    if sys.argv[1] == "test_readrom":
        test_readrom(bacon)
    elif sys.argv[1] == "test_readram":
        test_readram(bacon)
    elif sys.argv[1] == "test_writeram":
        test_writeram(bacon)
    elif sys.argv[1] == "read_flashid":
        read_flashid(bacon)
    elif sys.argv[1] == "rewrite_first_sector":
        rewrite_first_sector(bacon)
    bacon.power_control(False, False) # 0V
    bacon.spi_close()
