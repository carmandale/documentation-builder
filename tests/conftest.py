import pytest
from pathlib import Path
import sys

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

@pytest.fixture
def sample_data():
    """Provide sample test data"""
    return {
        'urls': {'http://test1.com', 'http://test2.com'},
        'paths': [Path('test/path1'), Path('test/path2')],
        'nested': {
            'set_data': {'item1', 'item2'}
        }
    } 