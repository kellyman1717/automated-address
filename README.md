# EVM Address Generator

This is a Python script to automate the generation of Ethereum Virtual Machine (EVM) addresses. It supports generating random EVM addresses with mnemonic seed phrases and custom "vanity" addresses with user-specified prefixes. The generated addresses, private keys, and seed phrases (where applicable) are saved to text files with sequential numbering.

## Features
- **Generate Random EVM Addresses**: Create a specified number of EVM addresses with private keys and mnemonic seed phrases, saved to `address_evm.txt`.
- **View Generated Addresses**: Display the contents of `address_evm.txt` to review previously generated addresses.
- **Generate Custom Vanity Addresses**: Create an EVM address with a custom prefix (e.g., `0x123`), saved to `custom_addr.txt`.
- **Multi-core Processing**: Uses Python’s `multiprocessing` to speed up vanity address generation.
- **Sequential Numbering**: Each address set in the output files is numbered for easy reference.

## Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

## Installation

1. **Clone or Download the Repository**
   - Clone this repository or download the script file (`evm_address_generator.py`).

2. **Install Dependencies**
   - Ensure you have the required libraries installed by running:
     ```bash
     pip install -r requirements.txt