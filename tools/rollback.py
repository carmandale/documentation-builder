from pathlib import Path
import shutil
import json
from datetime import datetime

def create_backup():
    """Create backup of current data"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path(f'backups/{timestamp}')
    
    # Backup data directory
    if Path('data').exists():
        shutil.copytree('data', backup_dir / 'data')
    
    # Backup configuration
    if Path('core/config.py').exists():
        shutil.copy('core/config.py', backup_dir / 'config.py')
    
    return backup_dir

def rollback_to_backup(backup_dir: Path):
    """Rollback to a specific backup"""
    if not backup_dir.exists():
        raise ValueError(f"Backup directory {backup_dir} does not exist")
    
    # Restore data directory
    if (backup_dir / 'data').exists():
        shutil.rmtree('data', ignore_errors=True)
        shutil.copytree(backup_dir / 'data', 'data')
    
    # Restore configuration
    if (backup_dir / 'config.py').exists():
        shutil.copy(backup_dir / 'config.py', 'core/config.py') 