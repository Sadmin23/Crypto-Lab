"use strict";

const { subtle } = require('crypto').webcrypto;
const e = require('express');
const { stringToBuffer, bufferToString, encodeBuffer, decodeBuffer } = require("./lib");


const generatePublicPrivateKeys = async () => {
    let keyPair = await subtle.generateKey(
        {
        name: "ECDSA",
        namedCurve: "P-521",
        },
        true,
        ['sign', 'verify']
    )

    let exportedPublicKey = await subtle.exportKey("jwk", keyPair.publicKey)
    let exportedPrivateKey = await subtle.exportKey("jwk", keyPair.privateKey)

    return {exportedPrivateKey, exportedPublicKey}
}

const signMessage = async (encoded, exportedPrivateKey) => {
    let signature = await subtle.sign(
        {
        name: "ECDSA",
        hash: { name: "SHA-384" },
        },
        exportedPrivateKey,
        encoded,
    );
    return signature
}

const verifySignature = async (encoded, signature, exportedPublicKey) => {
    let result = await subtle.verify(
        {
        name: "ECDSA",
        hash: { name: "SHA-384" },
        },
        exportedPublicKey,
        signature,
        encoded,
    );
    return result
}

const importKey = async (key, type) => {
    return await subtle.importKey(
        "jwk",
        key,
        {
            name: "ECDSA",
            namedCurve: "P-521",
        },
        true,
        [type]
    )
}

const getKeyPair = async () => {
    let keyPair = await generatePublicPrivateKeys()
    let privateKey = await importKey(keyPair.exportedPrivateKey, 'sign')
    let publicKey = await importKey(keyPair.exportedPublicKey, 'verify')
    return {privateKey, publicKey}
}

class user {
    constructor() {
        this.publicKey = null;
        this.privateKey = null;
    }

    async generateKeys() {
        let keyPair = await getKeyPair();
        this.publicKey = keyPair.publicKey;
        this.privateKey = keyPair.privateKey;
    }

    generateCertificate(owner, signer) {
        return {
            name: owner,
            CA: signer,
            publicKey: this.publicKey,
        }
    }

    async signMessage(message) {
        let encoded = stringToBuffer(JSON.stringify(message));
        let signature = await signMessage(encoded, this.privateKey);
        return signature;
    }

    async verifySignature(certificate, signature) {
        let encoded = stringToBuffer(JSON.stringify(certificate));
        const verification = await verifySignature(encoded, signature, this.publicKey);
        return verification;
    }
}


const encrypt = (name, key, message) => {

    console.log(`${name} is encrypting a message ...\n`);

    if (key.type === 'public')
        return encodeBuffer(message)
    else
        console.log('Failed to encrypt');
}

const decrypt = (name, key, ciphertext) => {

    console.log(`${name} is decrypting a ciphertext ...\n`);

    if (key.type === 'private')
        return bufferToString(decodeBuffer(ciphertext))
    else
        return console.log('Failed to decrypt');
}


(async () => {

    const RCA = new user();
    await RCA.generateKeys();

    const CA = new user();
    await CA.generateKeys();
    const certificateCA = CA.generateCertificate("CA", "RCA")

    const signatureCA = await RCA.signMessage(certificateCA)

    const verificationCA = await RCA.verifySignature(certificateCA, signatureCA)

    console.log('CA signature verification : ' + verificationCA + '\n');

    const Alice = new user();
    await Alice.generateKeys();
    const certificateAlice = Alice.generateCertificate("Alice", "CA")

    const signatureAlice = await CA.signMessage(certificateAlice);

    const verificationAlice = await CA.verifySignature(certificateAlice, signatureAlice);

    console.log('Alice signature verification : ' + verificationAlice + '\n');

    const Bob = new user();
    await Bob.generateKeys();
    const certificateBob = Bob.generateCertificate("Bob", "CA")

    const signatureBob = await CA.signMessage(certificateBob);
    const verificationBob = await CA.verifySignature(certificateBob, signatureBob)

    console.log('Bob signature verification :  '+verificationBob + '\n');

    let message = "This is a message that needs to reach Bob"

    let encryptedMessage = encrypt('Alice', Bob.publicKey, message)

    console.log('Encrypted Message by Alice: ' + encryptedMessage + '\n');

    let originalMessage = decrypt('Bob', Bob.privateKey, encryptedMessage)

    console.log('Decrypted message by Bob: ' + originalMessage + '\n');

    const Malory = new user();

    let capturedMessage = decrypt('Bob', Bob.privateKey, encryptedMessage)

    console.log('Message decrypted by Malory: ' + capturedMessage);

})();

