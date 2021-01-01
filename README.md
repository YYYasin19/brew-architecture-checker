# Brew Architecture Checker
This small script checks the supported bottled architectures for all currently installed brew formulaes.
Therefore one can have a look at all the supported/not-supported packages by for example the Apple Silicon M1 chip and decide to switch or not.

## Usage
```shell
python3 brew_check_availability.py --architecture="arm64_big_sur"
```
The `architecture`-flag is default and does not need to be set.
