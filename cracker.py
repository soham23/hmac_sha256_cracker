#!/usr/bin/env python3

import argparse
import os
import re
from hashlib import sha256
from hmac import new

## Functions

def generate_digest(secret_key: str, message: str) -> str:
    """
    Generate an HMAC-SHA256 digest using the supplied secret key and message.
    """
    return new(
        secret_key.encode("utf-8"),
        message.encode("utf-8"),
        sha256,
    ).hexdigest()

def generate_wordlist(file_name: str) -> list[str]:
    """
    Read a wordlist file and return a list of candidate secrets.
    """
    with open(file_name, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]

def validate_digest(digest: str) -> None:
    """
    Validate that the supplied digest is a valid SHA-256 hexadecimal string.
    """
    if len(digest) != 64:
        raise ValueError(f"Invalid SHA-256 digest: {digest}")

    if not re.fullmatch(r"[a-f0-9]{64}", digest):
        raise ValueError(f"Invalid SHA-256 digest: {digest}")

def validate_wordlist(file_name: str) -> None:
    """
    Ensure that the supplied wordlist file exists.
    """
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"Wordlist file does not exist: {file_name}")

def brute_secret(wordlist: list[str], message: str, digest: str) -> str | None:
    """
    Attempt to recover the HMAC secret using a dictionary attack.
    """
    for word in wordlist:
        if generate_digest(word, message) == digest:
            return word

    return None

def main() -> None:
    """
    Parse command-line arguments and perform the dictionary attack.
    """
    parser = argparse.ArgumentParser(
        description="Recover an HMAC-SHA256 secret using a dictionary attack."
    )

    parser.add_argument(
        "hash",
        help="Target HMAC-SHA256 digest",
    )
    parser.add_argument(
        "message",
        help="Plaintext message used to generate the digest",
    )
    parser.add_argument(
        "wordlist",
        help="Path to the dictionary file",
    )

    args = parser.parse_args()

    try:
        validate_digest(args.hash)
        validate_wordlist(args.wordlist)

        wordlist = generate_wordlist(args.wordlist)
        secret = brute_secret(wordlist, args.message, args.hash)

        if secret:
            print(f"Hash Cracked!!! Secret -> {secret}")
        else:
            print("Hash not cracked")

    except (ValueError, FileNotFoundError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
