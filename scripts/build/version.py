import sys
 
if not sys.version_info.major == 3 and sys.version_info.minor >= 7:
    print("Python version must be equal or higher than 3.7")
    sys.exit(1)

sys.exit(0)