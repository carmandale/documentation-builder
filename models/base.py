from datetime import datetime, UTC
from typing import List, Optional, Set
from pydantic import BaseModel, Field, ConfigDict

class CodeBlock(BaseModel):
    """Represents a code example in the documentation"""
    code: str
    description: Optional[str] = None
    language: str = "swift"  # Default to Swift for visionOS
    preview: str = Field(..., description="First 200 chars of code for quick reference")
    frameworks: List[str] = Field(default_factory=list)
    type: str = Field(
        default="other",
        description="Type of code example: ui_component, 3d_content, animation, app_structure, event_handling, immersive_space, other"
    )

class Topic(BaseModel):
    """Represents a section/topic in the documentation"""
    title: str
    level: int  # h1, h2, h3 etc.
    content: Optional[str] = None
    path: List[str] = Field(default_factory=list)  # Breadcrumb path to this topic

class DocumentationPage(BaseModel):
    """Represents a single documentation page"""
    title: str
    url: str
    introduction: Optional[str] = None
    code_blocks: List[CodeBlock]
    topics: List[Topic]
    related_links: List[dict] = Field(default_factory=list)
    category: Optional[str] = None  # Main category of the documentation
    frameworks_used: List[str] = Field(default_factory=list)  # All frameworks referenced
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    model_config = ConfigDict(
        ser_json={
            datetime: lambda dt: dt.isoformat()
        }
    )
    
    def __init__(self, **data):
        super().__init__(**data)
        # Aggregate frameworks from code blocks
        self.frameworks_used = list(set(
            framework
            for block in self.code_blocks
            for framework in block.frameworks
        ))
        # Try to determine category
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
    