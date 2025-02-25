# EVM Address Generator

Ini adalah bot Python yang dapat membuat address EVM dengan otomatis. Bot ini dapat membuat address EVM random dengan menyertakan **Private Key**, **Seed Phrase** ,dan **Custom Address** khusus dengan prefix yang ditentukan user. Address yang di generate, **Private Key**, dan **Seed Phrase** akan disimpan ke dalam file.

## Features
- **Generate Random Address EVM**: Membuat address secara acak dengan private key and mnemonic seed phrase, lalu disimpan di dalam `address_evm.txt`.
- **Menampilkan Hasil Random Address EVM**: Menampilkan isi dari `address_evm.txt`.
- **Generate Custom Address EVM**: Membuat custom address dengan custom prefix (contohnya, `0x123`), lalu disimpan di `custom_addr.txt`.
- **Multi-core Processing**: Menggunakan Python `multiprocessing` untuk mempercepat pembuatan custom address.

## Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

## Installation
1. **Clone atau Download Repository**
     ```bash
     git clone https://github.com/kellyman1717/automated-address.git
     ```

2. **Install Dependencies**
     ```bash
     pip install -r requirements.txt
