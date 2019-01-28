Solutions to the [Cryptopals] challenges in Python and Go.

## Versioning
Everything should work on Python 3.7 (or above) and Go 1.11 (or above).

## Usage
| Task | Command |
| ---- | ------- |
| Reformat `.py` files | `black .` |
| Reformat `.go` files | `gofmt -s -w .` |
| Typecheck `.py` files | `mypy .` |
| Run Python tests | `pytest` |
| Run Go tests | `go test` |

## Exceptions
- Problem 19 - Skipped; read file for info
- Problem 20 - Use `pytest -s` to inspect STDOUT

[Cryptopals]: https://cryptopals.com
