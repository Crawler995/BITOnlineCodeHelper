# BIT Online Code Helper
Test your code of "BIT Online coding homework" more easily and conveniently!

## Install
`pip install bit-online-code-helper`\
And you should confirm that `g++` command is available. For example, running `g++ -v` in the terminal to confirm.

## Feature
With this, you can test and commit your code which use only **2 seconds** totally:
1. Save your code in the editor (Ctrl + S)
2. Switch to show cmd or PowerShell window (Alt + Tab)
3. Press "↑" on your keyboard to automatically repeat your last test command
4. Press "Enter" on your keyboard, wait for test result!

## Usage
```shell script
# bch means 'BITOnline Code Helper'

# local code test
# -l means '--local'
bch -l [bit_online_problem_url] [source_file_url]

# online code test
# commit your code to BIT Online to test
# -o means '--online'
bch -o [bit_online_problem_url] [source_file_url]

# local and online code test
# automaticlly commit your code to BIT Online to test after local test passed
# -lo means '--local_online'
bch -lo [bit_online_problem_url] [source_file_url]

# e.g.
# bch -lo "http://lexue.bit.edu.cn/mod/programming/view.php?id=32165" "E:\coding\1.c"
```

## TODO
1. Use cache to store the problem info to avoid frequently request the website
2. Improve related features which I don't realize now
3. Fix bugs
