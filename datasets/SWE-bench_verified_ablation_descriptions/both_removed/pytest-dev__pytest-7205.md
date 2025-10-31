BytesWarning when using --setup-show with bytes parameter

When pytest prints the cached bytes parameter in the setup output, it implicitly calls str() on a bytes instance, causing a BytesWarning. Shouldn't it use a safe representation (e.g. saferepr) instead of str()?