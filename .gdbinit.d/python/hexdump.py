# Adapted from https://stackoverflow.com/a/9237555

import gdb
from curses.ascii import isgraph

def groups_of(iterable, size, first=0):
    first = first if first != 0 else size
    chunk, iterable = iterable[:first], iterable[first:]
    while chunk:
        yield chunk
        chunk, iterable = iterable[:size], iterable[size:]

class HexDump(gdb.Command):
    """Dump the hex at an address.

    hex-dump ADDR
    hex-dump ADDR LEN
    hex-dump ADDR@LEN
        ADDR -- An address or expression resolvable as an address. On its own,
                the size of the element at this address will be dumped.
        LEN -- In the 2nd form, dump this many bytes starting at the address.
                In the 3rd form, dump this many array elements starting at
                offset 0 of this address.
    """

    def __init__(self):
        super (HexDump, self).__init__ ("hex-dump", gdb.COMMAND_DATA)
        self.addr = 0 # address to dump
        self.byte_len = -1 # length in bytes

    def set_addr(self, addr):
        """Set self.addr.

        Args:
            addr (str): the new value for self.addr
        """
        self.addr = gdb.parse_and_eval(addr).cast(
                gdb.lookup_type("void").pointer())

    def set_byte_len(self, byte_len):
        """Set self.byte_len.

        Args:
            byte_len (int | str): the new value for self.byte_len
        """
        try:
            self.byte_len = int(gdb.parse_and_eval(str(byte_len)))
        except ValueError:
            raise gdb.GdbError("Byte count must be an integer value.")

    def one_arg(self, arg0):
        """Prepare for when there is 1 argument.

        Args:
            arg0 (str): the 1st argument
        """
        if "@" in arg0:
            split = arg0.split("@")
            if len(split) == 2:
                self.set_addr(split[0])
                try:
                    size = int(split[1]) * \
                            gdb.parse_and_eval(arg0).dereference().type.sizeof
                    self.set_byte_len(size) # size in bytes for array length
                except ValueError:
                    raise gdb.GdbError(
                            "Array element count must be an integer value.")
            else:
                raise gdb.GdbError(
                        "hex-dump takes an address and optional length.")
        else:
            self.set_addr(arg0)
            size = gdb.parse_and_eval(arg0).dereference().type.sizeof
            self.set_byte_len(size) # size in bytes for one unit

    def two_args(self, arg0, arg1):
        """Prepare for when there are 2 arguments.

        Args:
            arg0 (str): the 1st argument
            arg1 (str): the 2nd argument
        """
        self.set_addr(arg0)
        self.set_byte_len(arg1)

    def invoke(self, arg, from_tty):
        argv = gdb.string_to_argv(arg)
        if len(argv) == 1:
            self.one_arg(argv[0])
        elif len(argv) == 2:
            self.two_args(argv[0], argv[1])
        else:
            raise gdb.GdbError("hex-dump takes an address and length.")
        inferior = gdb.selected_inferior()
        align = gdb.parameter("hex-dump-align")
        width = gdb.parameter("hex-dump-width")
        mem = inferior.read_memory(self.addr, self.byte_len)
        pr_addr = int(str(self.addr), 16)
        pr_offset = width
        if align:
            pr_offset = width - (pr_addr % width)
            pr_addr -= pr_addr % width
        for grp in groups_of(mem, width, pr_offset):
            output = "0x%x: " % (pr_addr,) + "   " * (width - pr_offset) + \
                    " ".join(["%02X" % (ord(g),) for g in grp]) + \
                    "   " * (width - len(grp) if pr_offset == width else 0) + \
                    " " + " " * (width - pr_offset) + "".join(
                            [g.decode("utf-8") if isgraph(ord(g)) or g == b" " \
                                    else "." for g in grp])
            print(output)
            pr_addr += width
            pr_offset = width


class HexDumpAlign(gdb.Parameter):
    """Whether the hex dump is aligned on multiples of hex-dump-width."""

    def __init__(self):
        super (HexDumpAlign, self).__init__("hex-dump-align",
                                            gdb.COMMAND_DATA,
                                            gdb.PARAM_BOOLEAN)
        self.value = True

    set_doc = 'Determines if hex-dump always starts at an "aligned" address (on/off)'

    show_doc = "Hex dump alignment is currently"


class HexDumpWidth(gdb.Parameter):
    """The width of the displayed hex dump in a decimal number of bytes."""

    def __init__(self):
        super (HexDumpWidth, self).__init__("hex-dump-width",
                                            gdb.COMMAND_DATA,
                                            gdb.PARAM_INTEGER)
        self.value = 16
        self.saved_value = 16

    set_doc = 'Set the number of bytes per line of hex-dump (a positive integer)'

    def get_set_string(self):
        try:
            if int(self.value) < 1:
                self.value = self.saved_value
                raise gdb.GdbError(
                        "hex-dump-width must be a positive integer")
        except:
            raise gdb.GdbError("hex-dump-width must be a positive integer")
        self.saved_value = self.value
        return ""

    show_doc = "The number of bytes per line in hex-dump is"


HexDumpAlign()
HexDumpWidth()
HexDump()

