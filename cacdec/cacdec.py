# -*- coding: utf-8 -*-

"""
"""
from struct import pack

from construct import Struct, Const, Bytes, Int8ul, Int32ul, GreedyRange, Select, If, Int64ul, RepeatUntil
from cacdec.progressive import progressive_context_new, progressive_decompress, progressive_create_surface_context

RdpBitmapinfo = Struct(
    "unk_1" / Int32ul,
    "width" / Int32ul,
    "height" / Int32ul,
    "dst_step" / Int32ul,
    "unk_3" / Int32ul
)

SurfaceContext = Struct(
    "type" / Const(0, Int8ul),
    "info" / RdpBitmapinfo,
    "unknown" / Int32ul
)

SurfaceResult = Struct(
    "type" / Const(1, Int8ul),
    "status" / Int32ul
)

DecodingResult = Struct(
    "type" / Const(2, Int8ul),
    "status" / Int32ul
)

RectResult = Struct(
    "type" / Const(3, Int8ul),
    "status" / Int32ul
)

Bitmap = Struct(
    "type" / Const(4, Int8ul),
    "index" / Int32ul,
    "length" / Int32ul,
    "data" / Bytes(lambda this: this.length),
    "info" / RdpBitmapinfo,
    "have_point" / Int8ul,
    "point" / If(lambda this: this.have_point != 0, Int64ul)
)

CacdecDump = Struct(
    "magic" / Const(b"CacDec01"),
    "objects" / RepeatUntil(
        lambda x, lst, ctx: len(x._io.getbuffer()) == x._io.tell(),
        Select(
            SurfaceContext,
            SurfaceResult,
            DecodingResult,
            RectResult,
            Bitmap
        )

    )
)


def build_from_stream(stream, output_folder):
    cacdec_stream = CacdecDump.parse(stream)
    # first object must be a context
    if cacdec_stream.objects[0].type != 0:
        raise TypeError("cacdec file must start be a context object")
    width = cacdec_stream.objects[0].info.width
    height = cacdec_stream.objects[0].info.height
    codec = progressive_context_new(False)
    progressive_create_surface_context(codec, 0, 640, 480)

    screen = bytes(width*height*4)
    index = 0
    for i in cacdec_stream.objects:
        if i.type == 4:
            progressive_decompress(codec, i.info.width, i.info.height, i.info.dst_step, i.data, screen)
            file_path = "%s/windows.%s.data"%(output_folder, index)
            print("[+] writing frame of size %s %s into raw file data %s" % (width, height, file_path))

            screen_output = b''
            for i in range(0, height)[::-1]:
                curent_line = screen[i*width*4:(i+1)*width*4]
                line = b''
                for j in range(0, width):
                    line += curent_line[j*4:(j+1)*4][::-1]
                screen_output += line

            with open(file_path, "wb") as f:
                f.write(b"BM"+pack("<L", len(screen_output)+0x36)+b"\x00\x00\x00\x00\x32\x00\x00\x00\x28\x00\x00\x00"+pack("<L", width)+pack("<L", height)+b"\x01\x00\x20\x00\x00\x00\x00\x00"+pack("<L", len(screen_output))+b"\x00"*12+screen_output)
            index += 1

