Solutions to the [Cryptopals] challenges in Python and Go.

## Versioning
Everything should work on Python 3.7 (or above) and Go 1.11 (or above).

## Usage
| Task | Command |
| ---- | ------- |
| Reformat Python files | `$ black .` |
| Reformat Go files | `$ gofmt -s -w .` |
| Typecheck Python files | `$ mypy .` |
| Run Python tests | `$ pytest` |
| Run Go tests | `$ go test` |

## Exceptions
- Problem 19 - Skipped; read file for info
- Problem 20 - Use `pytest -s` to inspect STDOUT
- Problem 22 - Replace seconds with milliseconds for speed-up

[Cryptopals]: https://cryptopals.com
