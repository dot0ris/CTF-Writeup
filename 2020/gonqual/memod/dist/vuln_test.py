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
	
#integer type confusion
def integer_confusion(fname):
	#[REDACTED]
	p = process(["sudo", "-u", "runner", fname])
	p.close()
	return -1

#stack bof
def stack_bof(fname):
	#[REDACTED]
	p = process(["sudo", "-u", "runner", fname])
	p.close()
	return -1

#double free
def double_free(fname):
	#[REDACTED]
	p = process(["sudo", "-u", "runner", fname])
	p.close()
	return -1

#fsb
def fsb(fname):
	#[REDACTED]
	p = process(["sudo", "-u", "runner", fname])
	p.close()
	return -1


FUNCTION_LIST = [integer_confusion, stack_bof, double_free, fsb]

def vuln_test(fname):
	context.log_level = "error"
	passed = 0
	for f in FUNCTION_LIST:
		_print("[*] testing %s...\n"%f.__name__)
		c =  f(fname)
		_print(" exit code %d\n"%c)
		if c == 0 :
			passed += 1
	
	_print("[*] %d/%d test passed\n"%(passed, len(FUNCTION_LIST)))
	if passed < len(FUNCTION_LIST):
		_print("[+] vulnerability check fail..\n")
		return False
	else:
		_print("[+] vulnerability check passed!\n")
		return True