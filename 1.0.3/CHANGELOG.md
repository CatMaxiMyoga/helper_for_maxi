# UPDATE 1.0.3

## CHANGED

-  `append_clipboard.py`
    - Changed `pyperclip.copy(text.encode('utf-8').decode('utf-8'))` to `pyperclip.copy(text)` due to issues with the old method after 1.0.2