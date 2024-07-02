# RuntimeVerificationWithImperfectInformation

## Requirements

- Spot (https://spot.lrde.epita.fr/)

## How to run

Inside the terminal

```bash
$- python rvImpInf.py "<LTL>" "<AP>" "<Indistinguishability>" <file>
```

Just as an example

```bash
$- python rvImpInf.py "X a" "[a,b,c]" "[a,b]" test.txt
```

To test property presented in SEFM 2022 paper:
```bash
$- sh test_paper_property.sh
```
