# Bitcoin Transaction Decoding Assignment

## Overview
This assignment involves manually decoding a Bitcoin transaction hex and 
writing a Python decoder function to automate the process.

---

## Transaction Hex
0200000000010131811cd355c357e0e01437d9bcf690df824e9ff785012b6115dfae3d8e8b36c10100000000fdffffff0220a107000000000016001485d78eb795bd9c8a21afefc8b6fdaedf718368094c08100000000000160014840ab165c9c2555d4a31b9208ad806f89d2535e20247304402207bce86d430b58bb6b79e8c1bbecdf67a530eff3bc61581a1399e0b28a741c0ee0220303d5ce926c60bf15577f2e407f28a2ef8fe8453abd4048b716e97dbb1e3a85c01210260828bc77486a55e3bc6032ccbeda915d9494eda17b4a54dbe3b24506d40e4ff43030e00


---

## Task 1: Manual Decode
The manual decode is in manual-decode.md. Each field was decoded by reading 
the hex string from left to right, reversing bytes where little-endian 
format applies.

Note: The manual decode shows slight differences from the code output due 
to the complexity of little-endian byte conversion done by hand. The code 
output was verified against mempool.space and is accurate.

---

## Task 2: Python Decoder
The decoder.py file contains a Python function that automatically decodes 
any Bitcoin transaction hex.

### How it works:
- Reads the hex string from left to right using a position tracker
- Handles little-endian byte reversal automatically
- Supports both Legacy and SegWit transactions
- Extracts all transaction components including witness data
- Outputs structured, human readable results

### How to run:
python decoder.py


### Output:
The decoded output is saved in output.txt and includes:
- Version
- SegWit marker and flag
- All inputs with txid, vout, scriptSig and sequence
- All outputs with amounts in satoshis and BTC
- Witness data (signature and public key)
- Locktime

---

## Verification
Results verified against mempool.space:
https://mempool.space/tx/04f487fe9754a925c2e96492afeab47e7c839d0582eef80b3ecc9ca3afa05842

---

## Author
Mary Usaji