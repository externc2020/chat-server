import nacl.encoding
import nacl.signing

def test_1():
    # Generate a new random signing key
    signing_key = nacl.signing.SigningKey.generate()
    print(signing_key)

    # Sign a message with the signing key
    signed = signing_key.sign(b"Attack at Dawn")
    print(signed)

    # Obtain the verify key for a given signing key
    verify_key = signing_key.verify_key
    print(verify_key)

    # Serialize the verify key to send it to a third party
    verify_key_hex = verify_key.encode(encoder=nacl.encoding.HexEncoder)
    print(verify_key_hex)


    # Create a VerifyKey object from a hex serialized public key
    verify_key = nacl.signing.VerifyKey(verify_key_hex, encoder=nacl.encoding.HexEncoder)

    # Check the validity of a message's signature
    # Will raise nacl.exceptions.BadSignatureError if the signature check fails
    verified = verify_key.verify(signed)
    print(verified)