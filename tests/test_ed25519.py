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


def test_2():
    # Ed25519 is an elliptic curve signing algorithm using EdDSA and Curve25519.
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
    private_key = Ed25519PrivateKey.generate()
    print(private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.OpenSSH,
        encryption_algorithm=NoEncryption()
    ).decode())
    signature = private_key.sign(b"my authenticated message")
    print(signature.hex())
    public_key = private_key.public_key()
    print(public_key.public_bytes(
        encoding=Encoding.OpenSSH,
        format=PublicFormat.OpenSSH
    ).decode())
    # Raises InvalidSignature if verification fails
    public_key.verify(signature, b"my authenticated message")


def test_3():
    # admin sign A pubkey with pubkey + expiry_time
    # message, signature
    pass
