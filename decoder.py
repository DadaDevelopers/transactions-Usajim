def decode_transaction(hex_string):
    """
    Decode a Bitcoin transaction from hex format
    Handles both legacy and SegWit transactions
    
    Args:
        hex_string: Raw transaction hex
        
    Returns:
        Dictionary containing decoded transaction data
    """
    
    # Position tracker - keeps track of where we are in the hex string
    pos = 0
    
    def read_bytes(n):
        """Read n bytes (2n hex characters) from current position"""
        nonlocal pos
        data = hex_string[pos:pos + n * 2]
        pos += n * 2
        return data
    
    def read_varint():
        """Read a variable length integer"""
        first = int(read_bytes(1), 16)
        if first < 0xfd:
            return first
        elif first == 0xfd:
            return int(bytes.fromhex(read_bytes(2))[::-1].hex(), 16)
        elif first == 0xfe:
            return int(bytes.fromhex(read_bytes(4))[::-1].hex(), 16)
        else:
            return int(bytes.fromhex(read_bytes(8))[::-1].hex(), 16)
    
    def little_endian_to_int(hex_str):
        """Convert little-endian hex string to integer"""
        return int(bytes.fromhex(hex_str)[::-1].hex(), 16)
    
    def reverse_txid(hex_str):
        """Reverse bytes for txid display"""
        return bytes.fromhex(hex_str)[::-1].hex()
    
    # ===== START DECODING =====
    
    # 1. Version (4 bytes)
    version = little_endian_to_int(read_bytes(4))
    
    # 2. Check for SegWit (marker and flag)
    marker = hex_string[pos:pos + 2]
    is_segwit = False
    
    if marker == "00":
        is_segwit = True
        marker = read_bytes(1)  # 00
        flag = read_bytes(1)    # 01
    else:
        marker = None
        flag = None
    
    # 3. Input Count
    input_count = read_varint()
    
    # 4. Inputs
    inputs = []
    for i in range(input_count):
        txid = reverse_txid(read_bytes(32))
        vout = little_endian_to_int(read_bytes(4))
        script_length = read_varint()
        script_sig = read_bytes(script_length) if script_length > 0 else ""
        sequence = read_bytes(4)
        
        inputs.append({
            "txid": txid,
            "vout": vout,
            "script_length": script_length,
            "scriptSig": script_sig if script_sig else "empty",
            "sequence": sequence
        })
    
    # 5. Output Count
    output_count = read_varint()
    
    # 6. Outputs
    outputs = []
    for i in range(output_count):
        amount = little_endian_to_int(read_bytes(8))
        script_length = read_varint()
        script_pubkey = read_bytes(script_length)
        
        outputs.append({
            "amount_satoshis": amount,
            "amount_btc": amount / 100_000_000,
            "script_length": script_length,
            "scriptPubKey": script_pubkey
        })
    
    # 7. Witness Data (SegWit only)
    witness = []
    if is_segwit:
        for i in range(input_count):
            witness_count = read_varint()
            witness_items = []
            for j in range(witness_count):
                witness_length = read_varint()
                witness_data = read_bytes(witness_length)
                witness_items.append(witness_data)
            witness.append(witness_items)
    
    # 8. Locktime
    locktime = little_endian_to_int(read_bytes(4))
    
    # ===== BUILD RESULT =====
    result = {
        "version": version,
        "is_segwit": is_segwit,
        "marker": marker,
        "flag": flag,
        "input_count": input_count,
        "inputs": inputs,
        "output_count": output_count,
        "outputs": outputs,
        "witness": witness,
        "locktime": locktime
    }
    
    return result


def print_transaction(decoded):
    """Print decoded transaction in a readable format"""
    print("\n" + "="*50)
    print("       BITCOIN TRANSACTION DECODER")
    print("="*50)
    
    print(f"\nVersion:    {decoded['version']}")
    print(f"SegWit:     {decoded['is_segwit']}")
    
    if decoded['is_segwit']:
        print(f"Marker:     {decoded['marker']}")
        print(f"Flag:       {decoded['flag']}")
    
    print(f"\nInput Count: {decoded['input_count']}")
    for i, inp in enumerate(decoded['inputs']):
        print(f"\n  Input #{i + 1}:")
        print(f"    Previous TX Hash: {inp['txid']}")
        print(f"    Previous Output Index: {inp['vout']}")
        print(f"    Script Length: {inp['script_length']}")
        print(f"    ScriptSig: {inp['scriptSig']}")
        print(f"    Sequence: {inp['sequence']}")
    
    print(f"\nOutput Count: {decoded['output_count']}")
    for i, out in enumerate(decoded['outputs']):
        print(f"\n  Output #{i + 1}:")
        print(f"    Amount: {out['amount_satoshis']:,} satoshis ({out['amount_btc']:.8f} BTC)")
        print(f"    Script Length: {out['script_length']}")
        print(f"    ScriptPubKey: {out['scriptPubKey']}")
    
    if decoded['witness']:
        print(f"\nWitness Data:")
        for i, wit in enumerate(decoded['witness']):
            print(f"  Input #{i + 1} Witness:")
            for j, item in enumerate(wit):
                label = "Signature" if j == 0 else "Public Key"
                print(f"    {label}: {item}")
    
    print(f"\nLocktime: {decoded['locktime']:,}")
    print("\n" + "="*50)


# ===== TEST WITH PROVIDED TRANSACTION =====
tx_hex = "0200000000010131811cd355c357e0e01437d9bcf690df824e9ff785012b6115dfae3d8e8b36c10100000000fdffffff0220a107000000000016001485d78eb795bd9c8a21afefc8b6fdaedf718368094c08100000000000160014840ab165c9c2555d4a31b9208ad806f89d2535e20247304402207bce86d430b58bb6b79e8c1bbecdf67a530eff3bc61581a1399e0b28a741c0ee0220303d5ce926c60bf15577f2e407f28a2ef8fe8453abd4048b716e97dbb1e3a85c01210260828bc77486a55e3bc6032ccbeda915d9494eda17b4a54dbe3b24506d40e4ff43030e00"

decoded = decode_transaction(tx_hex)
print_transaction(decoded)