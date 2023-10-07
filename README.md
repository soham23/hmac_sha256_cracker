# HMAC-SHA256 Cracker

This tool can be used to crack secret keys that have been used to sign long messages with HMAC-SHA256 algorithms.

### Can't I just use hashcat?
Yes. In fact if your message is shorter than 51 bytes, I'd recommend using hashcat since it's a tried & tested tool. However, hashcat won't accept messages longer than 51 bytes.
Ref - https://hashcat.net/forum/thread-10233.html

## Usage
```sh
python3 cracker.py <hash> <message> <wordlist>
python3 cracker.py ee84159421888bdf29e40084524db8e4676e9b42e50394b017976df72e1f1460 "This is a super long message that will be rejected by hashcat because it is way too long." /usr/share/seclists/Passwords/xato-net-10-million-passwords-1000.txt
```

## Performance
![https://sohamgidwani.in/performance_edited.png](https://sohamgidwani.in/performance_edited.png)

## To Do
- [ ] Check out https://hashcat.net/forum/thread-6879.html to see if this script is actually worth maintaining
- [ ] Add requirements.txt
- [ ] Add a small wordlist that an user can use to just test out the script
- [ ] Find performance time for longer messages
