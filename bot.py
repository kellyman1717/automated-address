from eth_account import Account
import secrets
import os
import time
import sys
import re
import math
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
from mnemonic import Mnemonic

# Enable HD wallet features
Account.enable_unaudited_hdwallet_features()

def print_banner():
    banner1 = """
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║        AUTOMATE GENERATE EVM ADDRESS          ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """
    print(banner1)

def generate_evm_address():
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(strength=128)
    account = Account.from_mnemonic(mnemonic)
    address = account.address
    private_key = account.key.hex()
    return address, private_key, mnemonic

def count_address_sets(file_path):
    """Menghitung jumlah set address dalam file"""
    if not os.path.exists(file_path):
        return 0
    with open(file_path, 'r') as f:
        content = f.read()
        return content.count("Address:")

def save_address(file_path, address, private_key, mnemonic=None):
    """Menyimpan address dengan nomor urut berdasarkan file"""
    current_count = count_address_sets(file_path)
    current_count += 1
    with open(file_path, 'a') as f:
        if not mnemonic:
            f.write("\n")
        f.write(f"{current_count}. Address: {address}\n")
        f.write(f"Private Key: {private_key}\n")
        if mnemonic:
            f.write(f"Seed Phrase: {mnemonic}\n\n")
        else:
            f.write("\n" + "="*50 + "\n")

def is_hex_string(s):
    """Mengecek string yang hanya cocok dengan hex"""
    return bool(re.match('^[0-9a-fA-F]*$', s))

def estimate_time(prefix):
    """
    Estimasi waktu untuk mencari address custom berdasarkan prefix.
    Menggunakan probabilitas menemukan kecocokan: 1/(16^n) dimana n adalah panjang awalan.
    """
    if not prefix:
        return 0
    
    prefix = prefix.lower().replace('0x', '')
    if not is_hex_string(prefix):
        raise ValueError("Prefix hanya boleh berisi hex yang valid (0-9, a-f)")
    
    # Rata-rata waktu untuk mencari satu percobaan
    time_per_attempt = 0.0001
    
    # Kalkulasi kemungkinan
    attempts_needed = 16 ** len(prefix)
    
    # Rata-rata waktu untuk mencari semua percobaan
    estimated_time = attempts_needed * time_per_attempt
    
    # Menghitung waktu dengan multiprocessing
    cpu_count = multiprocessing.cpu_count()
    estimated_time = estimated_time / cpu_count
    
    return estimated_time

def generate_vanity_address(prefix):
    """Generate sekali percobaan untuk custom address."""
    try:
        private_key = secrets.token_hex(32)
        account = Account.from_key(private_key)
        address = account.address.lower()
        clean_address = address[2:]
        prefix_lower = prefix.lower()
        
        if len(prefix_lower) <= len(clean_address):
            if clean_address[:len(prefix_lower)] == prefix_lower:
                return {
                    'address': account.address,
                    'private_key': private_key
                }
        return None
    except Exception as e:
        print(f"Error dalam membuat custom address: {e}")
        return None

def find_vanity_address(prefix, max_time=None):
    if not prefix:
        raise ValueError("Prefix tidak boleh kosong")
    
    # Memvalidasi prefix
    prefix = prefix.lower().replace('0x', '')
    if not is_hex_string(prefix):
        raise ValueError("Prefix hanya boleh berisi hex yang valid (0-9, a-f)")
    
    if len(prefix) > 40:
        raise ValueError("Prefix tidak boleh lebih panjang dari 40 karakter")
    
    print(f"\nMembuat address dengan prefix: {prefix}")
    est_time = estimate_time(prefix)
    print(f"Estimasi Waktu: {est_time:.2f} detik")
    
    start_time = time.time()
    cpu_count = multiprocessing.cpu_count()
    print(f"Menggunakan {cpu_count} core CPU")
    
    attempts = 0
    found_address = None
    
    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        futures = []
        while True:
            if max_time and (time.time() - start_time) > max_time:
                print("\nWaktu limit tercapai.")
                executor.shutdown(wait=False)
                return None
            
            # Memasukkan batch tasks
            for _ in range(cpu_count * 2):
                futures.append(executor.submit(generate_vanity_address, prefix))
                attempts += 1
            
            # Mengecek hasil
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        found_address = result
                        executor.shutdown(wait=False)
                        elapsed_time = time.time() - start_time
                        print(f"\nBerhasil membuat address dalam {elapsed_time:.2f} detik!")
                        print(f"Total percobaan: {attempts}")
                        return found_address
                except Exception as e:
                    print(f"Error in worker: {e}")
                    continue
            futures = []
            
            # Menampilkan progress setiap detik
            elapsed = time.time() - start_time
            if int(elapsed) % 1 == 0:  # update setiap detik
                print(f"\rWaktu tersisa: {elapsed:.2f}s, Percobaan: {attempts}, Membuat: 0x{prefix}...", end="", flush=True)

def main():
    while True:
        print_banner()
        print("1. Buat EVM Address Sekarang")
        print("2. Cek Address EVM yang Sudah Dibuat")
        print("3. Generate Custom Address")
        print("0. Keluar")
        choice = input("Pilih opsi (1/2/3/0): ")
        print()

        if choice == '1':
            try:
                count = int(input("Masukkan jumlah address yang ingin dibuat: "))
                print()
                
                # Animasi loading
                print("Membuat address", end="")
                for _ in range(3):
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    time.sleep(1)
                print("\n")
                
                for _ in range(count):
                    address, private_key, mnemonic = generate_evm_address()
                    save_address('address_evm.txt', address, private_key, mnemonic)
                print(f"{count} address telah dibuat dan disimpan di address_evm.txt")
                print()
            except ValueError:
                print("Masukkan angka yang valid.")
        
        elif choice == '2':
            if os.path.exists('address_evm.txt'):
                with open('address_evm.txt', 'r') as f:
                    print(f.read())
            else:
                print("Kamu belum membuat address sebelumnya")
                print()
        
        elif choice == '3':
            banner2 = """
            ╔═══════════════════════════════════════════════╗
            ║                                               ║
            ║      AUTOMATE GENERATE CUSTOM EVM ADDRES      ║
            ║                                               ║
            ╚═══════════════════════════════════════════════╝
            """
            print(banner2)

            prefix = input("\nMasukkan prefix (tanpa 0x): ")
            
            while True:
                try:
                    # Estimasi waktu
                    est_time = estimate_time(prefix)
                    print(f"\nMembuat address dengan prefix: 0x{prefix}")
                    print(f"Estimasi untuk membuat address: {est_time:.2f} detik")
                    print(f"Note: Ini hanyalah estimasi. Bisa lebih cepat atau lebih lama.")
                    
                    proceed = input("\nApakah kamu ingin melanjutkan (y/n): ")
                    if proceed.lower() != 'y':
                        break
                    
                    # Menetapkan batas waktu maksimum menjadi 10 kali waktu yang diperkirakan
                    max_time = est_time * 10
                    
                    result = find_vanity_address(prefix, max_time)
                    if result:
                        print("\nSukses! Berhasil membuat address:")
                        print(f"Address: {result['address']}")
                        print(f"Private Key: {result['private_key']}")
                        
                        # Menyimpan ke dalam file dengan nomor urut
                        save_address('custom_addr.txt', result['address'], result['private_key'])
                        print("\nAddress disimpan di file custom_addr.txt")
                        break
                    else:
                        print(f"\nTidak dapat membuat address dengan prefix '0x{prefix}' dalam waktu yang ditentukan.")
                        retry = input("\nCoba ulang dengan prefix yang sama? (y/n): ")
                        if retry.lower() != 'y':
                            new_prefix = input("\nCoba dengan prefix lain? (y/n): ")
                            if new_prefix.lower() == 'y':
                                prefix = input("\nMasukkan prefix baru (tanpa 0x): ")
                                continue
                            break
                        print("\n" + "="*50)
                        continue
                
                except ValueError as e:
                    print(f"\nError: {e}")
                    retry = input("\nCoba ulang dengan prefix yang sama? (y/n): ")
                    if retry.lower() != 'y':
                        new_prefix = input("\nCoba dengan prefix lain? (y/n): ")
                        if new_prefix.lower() == 'y':
                            prefix = input("\nMasukkan prefix baru (tanpa 0x): ")
                            continue
                        break
                    print("\n" + "="*50)
                    continue
                
                except KeyboardInterrupt:
                    print("\n\nProses dihentikan oleh user.")
                    retry = input("\nCoba ulang dengan prefix yang sama? (y/n): ")
                    if retry.lower() != 'y':
                        new_prefix = input("\nCoba dengan prefix lain? (y/n): ")
                        if new_prefix.lower() == 'y':
                            prefix = input("\nMasukkan prefix baru (tanpa 0x): ")
                            continue
                        break
                    print("\n" + "="*50)
                    continue
        
        elif choice == '0':
            print("Exiting", end="")
            for _ in range(1,5):
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(1)
            print("\n")
            break
        
        else:
            print("Opsi tidak valid. Silakan pilih 1, 2, 3, atau 0.")

if __name__ == "__main__":
    main()