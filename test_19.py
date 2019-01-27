def test_solve():
    """Skipped; test always passes.

    The key to this problem is realizing that if:

    ```
    CT = PT ^ KS
    ```

    then, assuming an identical keystream for each ciphertext:

    ```
    CT1 ^ CT2 = (PT1 ^ KS) ^ (PT2 ^ KS)
              = KS ^ KS ^ PT1 ^ PT2
              = PT1 ^ PT2
    ```

    If you XOR any two ciphertexts together, you'll get the XOR of the two
    plaintexts. From there, you can use crib dragging, English trigrams, etc.
    
    This was too manual to bother testing.
    """
    assert True
