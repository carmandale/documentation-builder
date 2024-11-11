import pytest
import sys
from pathlib import Path

def run_tests():
    """Run the test suite"""
    # Add project root to path
    project_root = Path(__file__).parent
    sys.path.append(str(project_root))
    
    # Run tests with coverage
    args = [
        "tests",
        "-v",
        "--cov-report=term-missing",
        "--cov=analyzers"
    ]
    
    return pytest.main(args)

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code) 