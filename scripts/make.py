#!/usr/bin/env python3

import os
import itertools
import hashlib
import subprocess
import sys
import fileinput
import shutil
import fnmatch

############
#Options go here.
############

FREE_SPACE = 0xF00000

#############
#Options end here.
#############

def align_offset(offset):
	while (offset % 4) != 0:
		offset += 1
	return offset

def find_offset_to_put(rom, needed_bytes, start_loc):
	offset = start_loc
	found_bytes = 0
	while (found_bytes < needed_bytes):
		for i in range (0, needed_bytes):
			rom.seek(offset + i)
			byte = rom.read(1)
			if (byte):
				if (byte != b'\xFF'):
					offset += i + 1
					offset = align_offset(offset)
					found_bytes = 0
					break
				found_bytes += 1
			else:
				return 0
	return offset
	
def replace_line(file,searchString,replaceString):
    for line in fileinput.input(file, inplace=1):
        if searchString in line:
            line = replaceString + "\n"
        sys.stdout.write(line)

if (os.environ.get('DEVKITARM') == 'None'):
	print("...\nDevkitARM not found.")
	sys.exit(1)
else:
	from sys import platform
	if platform == "linux" or platform == "linux2":
		PATH = os.environ['DEVKITARM'] + "/bin"
		print("DevkitARM found!")
	elif platform == "win32":
		PATH = os.environ['DEVKITARM'].replace("/c", 'c:', 1) + "/bin"
		print("DevkitARM found!")
	else:
		PATH = os.environ['DEVKITARM'] + "/bin"
		print("DevkitARM found!")

PREFIX = '/arm-none-eabi-'
AS = (PATH + PREFIX + 'as')
CC = (PATH + PREFIX + 'gcc')
LD = (PATH + PREFIX + 'ld')
OBJCOPY = (PATH + PREFIX + 'objcopy')

SRC = 'src'
BUILD = 'build'

ASFLAGS = '-mthumb'
LDFLAGS = '-z muldefs --relocatable -T BPEE.ld -T linker.ld'
CFLAGS = '-g -O2 -Wall -mthumb -std=c11 -mcpu=arm7tdmi -march=armv4t -mno-thumb-interwork -fno-inline -fno-builtin -mlong-calls'

if os.path.exists(BUILD):
	shutil.rmtree(BUILD)

try:
	os.makedirs(BUILD)
except FileExistsError:
	pass

#Process c files
for file in os.listdir(SRC + '/'):
    if fnmatch.fnmatch(file, '*.c'):
        subprocess.call(CC + " " + CFLAGS + " -c " + SRC + "/" + file + " -o " + BUILD + "/" + file.rsplit( ".", 1 )[ 0 ]  + ".o")

#Process s files
for file in os.listdir(SRC + '/'):
    if fnmatch.fnmatch(file, '*.s'):
        subprocess.call(AS + " " + ASFLAGS + " -c " + SRC + "/" + file + " -o " + BUILD + "/" + file.rsplit( ".", 1 )[ 0 ]  + ".o")

#Link
FilesToLink = ""
for file in os.listdir(BUILD + '/'):
    if fnmatch.fnmatch(file, '*.o'):
        FilesToLink = FilesToLink + '"' + BUILD + "/" + file + '" '

subprocess.call(LD + " " + LDFLAGS + " -o " + '"' + BUILD + "/linked.o" + '" ' + FilesToLink)

subprocess.call(OBJCOPY + " -O " + 'binary "' + BUILD + "/linked.o" + '" "' + BUILD + '/output.bin"')

shutil.copyfile("rom.gba", "test.gba")
with open("test.gba", 'rb+') as rom:
	offset = find_offset_to_put(rom, os.stat("build/output.bin").st_size, align_offset(FREE_SPACE))
	rom.close()

replace_line("armips.asm",".org 0x08",".org " + hex(offset + 134217728))

#print(offset)

subprocess.call('armips "armips.asm" -sym "symbols.sym"')

subprocess.call("echo Project compiled and inserted!")
