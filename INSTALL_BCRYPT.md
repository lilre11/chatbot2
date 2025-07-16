# Installing bcrypt and Resolving Auth Routes Issues

## Problem
The `auth_routes.py` file has issues because the `bcrypt` package is not installed. This causes import errors and prevents the authentication system from working properly.

## Solution 1: Install bcrypt (Recommended)

### On Windows:
```bash
# First, install Microsoft C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Install with "C++ build tools" workload

# Then install bcrypt
pip install bcrypt
```

### On macOS:
```bash
# Install using Homebrew (if you have it)
brew install openssl

# Then install bcrypt
pip install bcrypt
```

### On Linux (Ubuntu/Debian):
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-dev libffi-dev

# Then install bcrypt
pip install bcrypt
```

### Alternative: Use pre-built wheels
If building from source fails, you can download pre-built wheels:

1. Go to https://www.lfd.uci.edu/~gohlke/pythonlibs/#bcrypt
2. Download the appropriate `.whl` file for your Python version
3. Install with: `pip install path/to/bcrypt-version-cpXX-win_amd64.whl`

## Solution 2: Use the Fallback Implementation (Current)

The current `auth_routes.py` includes a fallback implementation that uses SHA-256 hashing when bcrypt is not available. This works but is less secure than bcrypt.

### To use the fallback:
1. The code will automatically detect if bcrypt is available
2. If not, it will use SHA-256 with salt
3. No additional installation required

## Solution 3: Remove bcrypt dependency temporarily

If you want to remove the bcrypt dependency completely, you can modify `requirements.txt`:

```txt
# Comment out or remove this line:
# bcrypt==4.1.2
```

## Verification

After installing bcrypt, test the installation:

```python
import bcrypt
password = "test123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print("bcrypt is working!")
```

## Current Status

The `auth_routes.py` file is designed to work in both scenarios:
- **With bcrypt**: More secure, industry-standard password hashing
- **Without bcrypt**: Fallback to SHA-256 with salt (less secure but functional)

## Recommendation

1. **For Development**: Use the fallback implementation (current setup)
2. **For Production**: Install bcrypt for better security
3. **For Testing**: The fallback works fine for testing purposes

The authentication system will work regardless of whether bcrypt is installed, but installing bcrypt provides better security. 