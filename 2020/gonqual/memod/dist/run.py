#!/usr/bin/python3
import random
import hashlib
import tempfile
import sys,os
import signal
import base64
import subprocess
import pwd
from func_test import func_test
from vuln_test import vuln_test

MAX_PATCH_BYTE = 46
MAX_ADJACENT_PATCH_BYTE = 20

HASH_DIFFICULTY = 22
NONCE_LEN = 16
CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def _print(content):
	print(content,  end = "")
	sys.stdout.flush()

def check_vaild_patch(bin1, bin2):
	# check patch range
	bin_diff = bytes([x ^ y for x,y in zip(bin1,bin2)])
	# only patch in 0x400897 ~ 0x401240 allowed!
	diff_outrange = bin_diff[:0x897] + bin_diff[0x1240:]
	if len(diff_outrange.replace(b"\x00", b"")) != 0:
		_print("[-] patched byte on unallowed range!\n")
		return False

	# check patch cnt
	patched_byte = len(bin_diff.replace(b"\x00", b""))
	if patched_byte > MAX_PATCH_BYTE:
		_print("[-] Too many patched byte!\n")
		_print("[-] max %d byte, but %d byte patched\n"%(MAX_PATCH_BYTE, patched_byte))
		return False

	# check max adjacent
	max_adjacent = max(bin_diff.split(b"\x00"), key=len)
	if len(max_adjacent) > MAX_ADJACENT_PATCH_BYTE:
		_print("[-] Too long adjacent patched byte!\n")
		_print("[-] max %d byte, but %d byte is adjacent\n"%(MAX_ADJACENT_PATCH_BYTE, len(max_adjacent)))
		return False

	else:
		_print("[+] patch check passed!\n")
		return True

def check_functionality(fname):
	return func_test(fname)

def check_vuln(fname):
	return vuln_test(fname)

if __name__ == "__main__":
	with open("./mms", "rb") as f:
		orig_bin = f.read()
	signal.alarm(60)
	
	try:
		nonce = "".join(random.sample(CHARSET, NONCE_LEN))
		_print("Give me an alphanumeric string S such that md5( S || %s ) has %d leading zero bits.\n"%(nonce, HASH_DIFFICULTY))
		s = sys.stdin.readline().strip()
		if s.isalnum() == False:
			_print("[-] given string is not alphanumeric...\n")
			exit(1)
		
		h = hashlib.md5()
		h.update((s + nonce).encode())
		md = h.digest()
		
		for i in range(HASH_DIFFICULTY):
			byte_idx = i // 8
			bit_idx = 7 - i % 8
			
			if md[byte_idx] & (1 << bit_idx):
				_print("[-] PoW fail...\n")
				exit(1)
				
		_print("[+] PoW solved!\n")
		
		_print("[*] give me pathced file :")
		patch_bin = sys.stdin.buffer.read(len(orig_bin))
		if not check_vaild_patch(orig_bin, patch_bin):
			exit(1)
		f = tempfile.NamedTemporaryFile(delete=False)
		f.write(patch_bin)
		f.close()

		os.chmod(f.name,0o777)

		if check_functionality(f.name) and check_vuln(f.name):
			_print("[+] congratulation! here's your flag\n")
			_print(open("flag","r").read())

		os.unlink(f.name)
	except Exception as e :
		_print("[!] error occured! please report it to admin\n")
		_print(e)