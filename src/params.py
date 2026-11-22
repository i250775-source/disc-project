#  R             = 0775 + 0740 + 0848 = 2363
#  Pair number   = R mod 190 = 83  ->  (i, j) = (4, 18)
#  Department A  = top-20[4]    
#  Department B = top-20[18]
#  Random nets   = 20 + (R mod 31) = 27
#  Swap attempts = (5 + (R mod 6)) x edges = 10 x edges
#  Seed          = R = 2363

ROLL_NUMBERS = ["25I-0775", "25I-0740", "25I-0848"]


def compute_R(roll_numbers):
    return sum(int(roll[-4:]) for roll in roll_numbers)


def pair_from_number(pair_number, n=20):
    index = 0
    for i in range(n):
        for j in range(i + 1, n):
            if index == pair_number:
                return i, j
            index += 1
    raise ValueError("pair number out of range")


R = compute_R(ROLL_NUMBERS)                 
PAIR_NUMBER = R % 190                      
PAIR_I, PAIR_J = pair_from_number(PAIR_NUMBER)  
NUM_RANDOM_NETWORKS = 20 + (R % 31)         
SWAP_MULTIPLIER = 5 + (R % 6)             
SEED = R                                


if __name__ == "__main__":
    print("R                  =", R)
    print("Pair number        =", PAIR_NUMBER, "->", (PAIR_I, PAIR_J))
    print("Random networks    =", NUM_RANDOM_NETWORKS)
    print("Swap attempts      =", SWAP_MULTIPLIER, "x edges")
    print("Seed               =", SEED)
