#!/bin/python3
from hmac import new
from hashlib import sha256
import argparse
import re
import os

## Functions

def generate_digest(secret_key, message):
	digest = new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), sha256).hexdigest()
	return str(digest)

def generate_wordlist(file_name):
	f = open(file_name, "r")
	lines = f.readlines()
	f.close()
	wordlist = [x.strip() for x in lines]
	return wordlist

def assert_digest(digest):
	if(len(digest) != 64):
		print(f"Invalid sha256 digest -> {digest}")
		exit()
	if(re.findall('^[a-z0-9]+$', digest) == []):
		print(f"Invalid sha256 digest -> {digest}")
		exit()

def assert_wordlist(file_name):
	if(not os.path.isfile(file_name)):
		print(f"Invalid file or file doesn't exist -> {file_name}")
		exit()

def brute_secret(wordlist, message, digest):
	for word in wordlist:
		cur_digest = generate_digest(word, message)
		if(cur_digest == digest):
			return word
	return None

## Parse Command-Line Arguments
parser = argparse.ArgumentParser()
parser.add_argument("hash", help="Digest or hash you want to crack")
parser.add_argument("message", help="Plaintext message that has been signed using HMAC-SHA256")
parser.add_argument("wordlist", help="Wordlist file you want to use to brute-force the secret")

args = parser.parse_args()
digest = args.hash
message = args.message
wordlist_file = args.wordlist

## Check if arguments are valid
assert_digest(digest)
assert_wordlist(wordlist_file)

## Crack the digest
wordlist = generate_wordlist(wordlist_file)
secret = brute_secret(wordlist, message, digest)
if(secret != None):
	print(f"Hash Cracked!!! Secret -> {secret}")
else:
	print("Hash not cracked")