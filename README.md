
# ULC-MILP

MILP-Based Differential Characteristics Search Problem for Block Cipher ULC


## Source Code

There are five files in this source code.
- Ineq_Reduction.py 
- ULC.py
- Outer_ULC_64_15.lp
- Inner_ULC_64_15.lp
- 15-round_Differential_Characteristic.txt
- ULC_in_out.py
- 13-round_Differential_Distinguisher.txt
- 12-round_Differential_Distinguisher.txt

## Generation and Reduction of Linear Inequalities

- First, Ineq_Reduction.py generates linear inequalities. Then, minimize the linear inequalities using GUROBI (to reduce the number of active S-boxes or to optimize the probability of differential characteristics).

- The command 'python Ineq_Reduction.py ULC Sbox GUROBI -' gives the list of minimized linear inequalities to reduce the number of active S-boxes.

- The command 'python Ineq_Reduction.py ULC prob GUROBI -' provides the list of minimized linear inequalities to optimize the probability of differential characteristics.


## MILP model to minimize the number of active S-boxes and optimize the probability of differential characteristics

- ULC.py is used to model the MILP problem and solve it using GUROBI. Linear inequalities generated in the previous section have to be updated in this file. This file generates two modules outer and inner. The outer module minimizes the number of active S-boxes while the inner module search for differential characteristics with high probability. Both these modules are interfaced together and the user need not run these separately.

- ULC.py takes seven arguments. The first argument defines block size, the second argument defines the number of rounds, the third argument defines the minimum number of active S-boxes, the fourth argument defines whether the difference of some rounds is fixed or not, the fifth argument defines the number of trails to find, the sixth argument defines possible/impossible differential characteristics and seventh argument is used to define the solver.

- High probability differential characteristic for 15-round ULC is searched using the following command:
```bash
    python ULC.py 64 15 15 no_fix 1 possible GUROBI
```

- The differential characteristic is mentioned in the 15-round_Differential_Characteristic.txt file.

  ## Key Recovery Distinguishers

  - ULC_in_out.py is used to generate 13-round and 12-round differential distinguishers as follows:
    ```bash
        python ULC_in_out.py 64 13 13 no_fix 1 possible GUROBI
        python ULC.py 64 12 12 no_fix 1 possible GUROBI
    ```
    as given in 13-round_Differential_Distinguisher.txt and 12-round_Differential_Distinguisher.txt files.
