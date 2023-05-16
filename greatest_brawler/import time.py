import time

def add_one_to_reach_target(target_number):
    counter = 0
    start_time = time.time()

    while counter < target_number:
        counter += 1

    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time

target_number = 1000000
elapsed_time = add_one_to_reach_target(target_number)
print(f'Time taken to reach {target_number} by adding one: {elapsed_time} seconds')
