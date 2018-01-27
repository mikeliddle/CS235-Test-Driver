# Pass Off Automator

This directory, its folders, and scripts are a simple tool that I have mocked up to streamline pass off. It is simple, linear, and what I will use. I cannot guarantee that I will provide updates as we go, but if I do add to it I will share it with you. Feel free to read through the scripts and modify it to suit your needs.

## The Directories

There are 5 directories to keep things organized:

- `diffs/`: text files containing the results of the diffs will be stored here
- `keys/`: `run.sh` expects key_files for comparison to live here
- `output\`: all out_files will be moved here immediately after they have been written
- `src\`: put all student source code (except their main) in this directory (I don't have this part automated)
- `tests\`: the files containing instructions to main live here. The compiled executable will also be created here since the main relies on the files being in the same directory.

## `run.sh`

`run.sh` has a few phases:

1. __Setup__: It copies an unmodified main into `src/` for fairness to all students.
2. __Compilation__: It compiles source code. If a student relies on a different version, change the `VERSION` variable in `run.sh`, the default is `-std=c++14`
3. __Execution__: The script changes its working directory and "moves" into the `tests/` folder to run the compiled program. Upon completion, the working directory is changed back to the same directory as `run.sh`. It then actually moves all the `out_file*.txt` to the `out_put/` directory.
4. __Comparison__: `sdiff` is run on the pairs of files in `keys/` and `output/`. The verbose output is piped into text files found int `diffs/`, and a short sentence is reported via terminal.
5. __Clean Up__: `run.sh` will finally prompt if you would like to clean up the pass off environment (see below for example) and if you respond `Y`, then the `clean.sh` script will run. This script deletes the contents of `diffs/`, `output/`, and `src/`. If you'd like to check the diff files, simply respond `N` and run `clean.sh` at your leisure.

## Example Execution

```bash
matt@ubuntu:~/code/cs235/lab1/passoff$ ./run.sh
Compilation succeeded!

Moved to /home/matt/code/cs235/lab1/passoff/tests

Running Student Program
--------
==18890== Memcheck, a memory error detector
==18890== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
==18890== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
==18890== Command: ./program
==18890==
Reading file1.txt...
'useAbilities' flag set to true
Battles for file 0 will involve the 'useAbility()' and 'regenerate()' functions
Beginning out_file1.txt write
File write complete

Reading file2.txt...
Beginning out_file2.txt write
File write complete

Reading file3.txt...
Beginning out_file3.txt write
File write complete

Reading file4.txt...
Beginning out_file4.txt write
File write complete

Reading file5.txt...
'useAbilities' flag set to true
Battles for file 4 will involve the 'useAbility()' and 'regenerate()' functions
Beginning out_file5.txt write
File write complete

end
==18890==
==18890== HEAP SUMMARY:
==18890==     in use at exit: 18,944 bytes in 1 blocks
==18890==   total heap usage: 366 allocs, 365 frees, 114,680 bytes allocated
==18890==
==18890== 18,944 bytes in 1 blocks are still reachable in loss record 1 of 1
==18890==    at 0x402D17C: malloc (in /usr/lib/valgrind/vgpreload_memcheck-x86-linux.so)
==18890==    by 0x40BB5BA: ??? (in /usr/lib/i386-linux-gnu/libstdc++.so.6.0.21)
==18890==    by 0x400F364: call_init.part.0 (dl-init.c:72)
==18890==    by 0x400F48D: call_init (dl-init.c:30)
==18890==    by 0x400F48D: _dl_init (dl-init.c:120)
==18890==    by 0x4000AFE: ??? (in /lib/i386-linux-gnu/ld-2.23.so)
==18890==
==18890== LEAK SUMMARY:
==18890==    definitely lost: 0 bytes in 0 blocks
==18890==    indirectly lost: 0 bytes in 0 blocks
==18890==      possibly lost: 0 bytes in 0 blocks
==18890==    still reachable: 18,944 bytes in 1 blocks
==18890==         suppressed: 0 bytes in 0 blocks
==18890==
==18890== For counts of detected and suppressed errors, rerun with: -v
==18890== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
--------

Moved to /home/matt/code/cs235/lab1/passoff

Running Diff
--------
key_file1.txt and out_file1.txt are identical
key_file2.txt and out_file2.txt are identical
key_file3.txt and out_file3.txt are identical
key_file4.txt and out_file4.txt are identical
key_file5.txt and out_file5.txt are identical
--------

Clean up the passoff environment? [Y/N]? Y
removed 'diffs/diff_file1.txt'
removed 'diffs/diff_file2.txt'
removed 'diffs/diff_file3.txt'
removed 'diffs/diff_file4.txt'
removed 'diffs/diff_file5.txt'
removed 'output/out_file1.txt'
removed 'output/out_file2.txt'
removed 'output/out_file3.txt'
removed 'output/out_file4.txt'
removed 'output/out_file5.txt'
removed 'src/Archer.cpp'
removed 'src/Archer.h'
removed 'src/Arena.cpp'
removed 'src/Arena.h'
removed 'src/ArenaInterface.h'
removed 'src/Cleric.cpp'
removed 'src/Cleric.h'
removed 'src/Fighter.cpp'
removed 'src/Fighter.h'
removed 'src/FighterInterface.h'
removed 'src/lab1_main.cpp'
removed 'src/Robot.cpp'
removed 'src/Robot.h'
matt@ubuntu:~/code/cs235/lab1/passoff$ 
```
