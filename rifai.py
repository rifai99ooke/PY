import sys
import time
import os
os.system('cls')

def jalanin_lirik () :
    lirik = [
        ("Tahukah dirimu", 0.1),
        ("tahukah hatimu?", 0.1),
        ("Berulang kuketuk", 0.09),
        ("aku mencintamu", 0.1),
        ("Tapi dirimu", 0.1),
        ("tak pernah sadari", 0.1),
        ("Akuuuuuuuuuuuuuuuu yang jatuh cinta", 0.2),
    ]

    delay = [2, 1, 1, 2, 1, 1, 8,]
    print("\n==Aku Yang Jatuh Cinta==")
    time.sleep(2)
    for i, (baris_lagu, delay_karakter) in enumerate(lirik):
        for karakter in baris_lagu :
            print(karakter, end='')
            sys.stdout.flush()
            time.sleep(delay_karakter)
        time.sleep(delay[i])
        print('')
    print("// by Ahmad Rifai")  


jalanin_lirik()