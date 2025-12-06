# Setup-Packager
What is Setup-Packager(SP)?
Setup-Packager is a tool that is coded with Python and it helps you create a setup binary for your project

# Contribution
You can do `anything` with SP but you can not become an offical member of RandomX42069(RandomX)'s programmers group

# Usage Example
Example 1:
```shell
python ./src/cmain.py
```

Example 2:
```shell
python ./src/cmain.py randomDir
```

Example 3: this example uses --use-gcc. It will call GCC to compile the _setup.c and removes the _setup.c immediately after a success compiliation
```shell
python ./src/cmain.py --use-gcc
```

Example 4: same as example 3 but uses clang
```shell
python ./src/cmain.py --use-clang
```

# Tests
`test.ps1`: Success
`test2.ps1`: Success
`test3.ps1`: Failed because I don't use standalone gcc

# License
MIT License