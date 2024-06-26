const axios = require('axios');
const crypto = require('crypto');
const { promisify } = require('util');
const base64url = require('base64url');

const URL_BASE = 'http://localhost:8000';

class AES_256_Encrypter {
  constructor() {
    this.publicKey = null;
  }

  async getPublicKey() {
    try {
      const response = await axios.get(`${URL_BASE}/get_public_key`);
      this.publicKey = response.data;
      return this.publicKey;
    } catch (error) {
      console.error('Error fetching public key:', error);
      throw error;
    }
  }

  async encryptPasswordWithPublicKey(password) {
    const publicKey = await this.getPublicKey();
    const encryptedPassword = crypto.publicEncrypt(
      {
        key: publicKey,
        padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
        oaepHash: 'sha256',
      },
      Buffer.from(password)
    );
    return encryptedPassword;
  }
}

const encrypter = new AES_256_Encrypter();

async function registerNewUser(username, email, password) {
  const url = `${URL_BASE}/register`;
  try {
    const encryptedPassword = await encrypter.encryptPasswordWithPublicKey(password);
    const encryptedPasswordBase64 = base64url(encryptedPassword);

    const requestBody = {
      username: username,
      email: email,
      hashed_password: encryptedPasswordBase64,
    };

    const result = await axios.post(url, requestBody);
    console.log('response:', result.data);
  } catch (error) {
    if (error.response) {
      console.error('HTTP error occurred:', error.response.status, error.response.data);
    } else {
      console.error('Other error occurred:', error.message);
    }
  }
}

registerNewUser('pepo gracia', 'pepogracia@example.com', 'hello123');
