from datetime import datetime, UTC
from typing import List, Dict, Optional, Set
from pydantic import BaseModel, Field, ConfigDict
from pathlib import Path

class Topic(BaseModel):
    """Represents a section/topic in the documentation"""
    title: str
    level: int  # h1, h2, h3 etc.
    content: Optional[str] = None
    path: List[str] = Field(default_factory=list)  # Breadcrumb path to this topic

class CodeBlock(BaseModel):
    """Represents a code example from documentation"""
    code: str
    description: Optional[str] = None
    language: str = "swift"  # Default to Swift for visionOS
    preview: str = Field(..., description="First 200 chars of code for quick reference")
    frameworks: List[str] = Field(default_factory=list)
    type: str = Field(
        default="other",
        description="Type of code example: ui_component, 3d_content, animation, app_structure, event_handling, immersive_space, other"
    )

class CodePattern(BaseModel):
    """Represents a reusable code pattern"""
    pattern_type: str = Field(..., description="Type of pattern (e.g., animation, transform)")
    code: str
    source_file: str  # Track where we found it
    frameworks: List[str]
    prerequisites: List[str] = Field(default_factory=list)
    related_concepts: List[str] = Field(default_factory=list)
    validation_examples: List[str] = Field(default_factory=list)
    usage_count: int = 0  # Track how often we see this pattern
    variations: List[str] = Field(default_factory=list)  # Track variations of the pattern

class ConceptRelationship(BaseModel):
    """Represents a relationship between two concepts"""
    source: str
    target: str
    relationship_type: str
    strength: float = 1.0

class ValidationTest(BaseModel):
    """Represents a validation test for a code pattern"""
    pattern_id: str
    test_code: str
    expected_behavior: str
    frameworks: List[str]

class DocumentationPage(BaseModel):
    """Represents a single documentation page"""
    title: str
    url: str
    introduction: Optional[str] = None
    code_blocks: List[CodeBlock]  # Keep the original working attribute
    code_patterns: Dict[str, CodePattern] = Field(default_factory=dict)  # Add new functionality
    topics: List[Topic]
    relationships: List[ConceptRelationship] = Field(default_factory=list)
    validation_tests: List[ValidationTest] = Field(default_factory=list)
    category: Optional[str] = None
    frameworks_used: List[str] = Field(default_factory=list)
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    model_config = ConfigDict(
        ser_json={
            datetime: lambda dt: dt.isoformat()
        }
    )
    
    def __init__(self, **data):
        super().__init__(**data)
        # Aggregate frameworks from both code_blocks and code_patterns
        frameworks = set()
        
        # From code_blocks
        for block in data.get('code_blocks', []):
            frameworks.update(block.frameworks)
            
        # From code_patterns
        for pattern in data.get('code_patterns', {}).values():
            frameworks.update(pattern.frameworks)
            
        self.frameworks_used = list(frameworks)
        self._determine_category()
    
    def _determine_category(self):
        """Determine the main category of the documentation"""
        title_lower = self.title.lower()
        if '3d' in title_lower or 'reality' in title_lower:
            self.category = '3D_Content'
        elif 'immersive' in title_lower:
            self.category = 'Immersive_Experience'
        elif 'window' in title_lower or 'view' in title_lower:
            self.category = 'UI_Components'
        elif 'first' in title_lower or 'getting started' in title_lower:
            self.category = 'Getting_Started'
        else:
            self.category = 'Other'
    
class ProjectResource(BaseModel):
    """Represents a downloadable project resource"""
    title: str
    url: str
    download_url: Optional[str] = None
    local_path: Optional[Path] = None
    downloaded: bool = False
    documentation_url: Optional[str] = None
    documentation_title: Optional[str] = None
    
    def mark_downloaded(self, path: Path):
        self.local_path = path
        self.downloaded = True
    
    def model_dump(self, *args, **kwargs):
        """Pydantic v2 compatible dump method"""
        d = super().model_dump(*args, **kwargs)
        if d.get('local_path'):
            d['local_path'] = str(d['local_path'])
        return d
    
    def dict(self, *args, **kwargs):
        """Legacy dict method for compatibility"""
        return self.model_dump(*args, **kwargs)
    