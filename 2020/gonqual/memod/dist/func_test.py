#!/usr/bin/python3

import tempfile
import sys,os
import signal
import base64
import subprocess
import hashlib
from pwn import *

def _print(content):
	print(content,  end = "")
	sys.stdout.flush()

#test command listing
def list_command(fname):
	#[REDACTED]
	p = process(["sudo", "-u", "runner", fname])
	p.close()
	return (-1, False)

#test memo make
def make_memo(fname):
	#[REDACTED]
	p = process(["sudo", "-u", "runner", fname])
	p.close()
	return (-1, False)

#test memo read
def read_memo(fname):
	#[REDACTED]
	p = process(["sudo", "-u", "runner", fname])
	p.close()
	return (-1, False)

#test memo write
def write_memo(fname):
	#[REDACTED]
	p = process(["sudo", "-u", "runner", fname])
	p.close()
	return (-1, False)

#test memo close
def close_memo(fname):
	#[REDACTED]
	p = process(["sudo", "-u", "runner", fname])
	p.close()
	return (-1, False)


FUNCTION_LIST = [list_command, make_memo, read_memo, write_memo, close_memo]

def func_test(fname):
	context.log_level = "error"
	passed = 0
	for f in FUNCTION_LIST:
		_print("[*] testing %s...\n"%f.__name__)
		c, r =  f(fname)
		_print(" exit code %d\n"%c)
		if r:
			_print(" result matched\n")
		else:
			_print(" result unmatched with ref binary\n")
		if c == 0 and r:
			passed += 1
	
	_print("[*] %d/%d test passed\n"%(passed, len(FUNCTION_LIST)))
	if passed < len(FUNCTION_LIST):
		_print("[+] functionality check fail..\n")
		return False
	else:
		_print("[+] functionality check passed!\n")
		return True