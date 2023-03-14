import seed_generator as sg
import time
import multiprocessing as mp

def generate_address(address_string: str, index: int):
    mnemonic = sg.bytes_to_mnemonic(sg.generate_bytes())
    seed = sg.mnemonic_to_seed(mnemonic)
    seed = sg.AugSchemeMPL.key_gen(seed)
    for i in range(0, index):
        address = sg.get_observer_address(seed, [i])
        if address.endswith(address_string):
            print(mnemonic)
            print(f'Address [{i}]: {address}')
            return True

def main(search: str, index: int, threads: int):
    try:
        start_time = time.time()
        found = False
        count = 0
        tasks = []
        # rewrite for multiprocessing
        while not found:
            # processes = [mp.Process(target=generate_address, args=(address_string, index)) for i in range(0, 6)]
            # for p in processes:
            #     p.start()
            # for p in processes:
            #     p.join()
            pool = mp.Pool(processes=threads)
            results = [pool.apply_async(generate_address, (search, index)) for i in range(0, threads)]
            for r in results:
                if r.get():
                    found = True
                    break
            pool.close()
            pool.join()
            count += 1
            
            print(count)
            

        print(f"Found in {time.time() - start_time} seconds.")
    except KeyboardInterrupt:
        exit()

if __name__ == "__main__":
    search = input("Enter vanity string to search (recommended 5 characters or less): ")
    index = int(input("Enter derivation index to search to (500 is good): "))
    threads = int(input("Enter number of threads to use (as many as your cpu can handle): "))
    main(search, index, threads)