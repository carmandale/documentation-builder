"""Script to update README.md with current project structure"""
from pathlib import Path
import subprocess

def get_project_structure():
    """Get actual project structure using tree command"""
    result = subprocess.run(['tree', '-L', '2', '--dirsfirst'], 
                          capture_output=True, text=True)
    return result.stdout

def update_readme():
    """Update README.md with current structure"""
    readme = Path('README.md')
    content = readme.read_text()
    
    # Find project structure section
    start = content.find('## Project Structure')
    end = content.find('##', start + 1)
    
    # Get current structure
    structure = get_project_structure()
    
    # Create new section
    new_section = f"""## Project Structure
Current implementation:

```
{structure}
```
"""
    
    # Update content
    new_content = content[:start] + new_section + content[end:]
    
    # Backup original
    readme.rename(readme.with_suffix('.md.bak'))
    
    # Write new content
    readme.write_text(new_content)

if __name__ == '__main__':
    update_readme() 