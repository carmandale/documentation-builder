# Core API Reference

## DocumentationAnalyzer

```python
from core.documentation_analyzer import DocumentationAnalyzer

analyzer = DocumentationAnalyzer(knowledge_dir: Path)
```

### Methods

#### analyze_documentation
```python
async def analyze_documentation(self, url: str) -> Dict[str, Any]
```
Analyzes documentation content from a URL.

**Parameters:**
- `url`: Documentation URL to analyze

**Returns:**
- Analysis results including patterns and relationships

## KnowledgeBase

```python
from core.knowledge_base import VisionOSKnowledgeBase

kb = VisionOSKnowledgeBase(data_dir: Path = Path('data/knowledge'))
```

### Methods

#### build_from_analysis
```python
def build_from_analysis(self, pattern_data: Dict[str, Any])
```
Builds knowledge base from analysis results.

**Parameters:**
- `pattern_data`: Dictionary containing pattern analysis data

#### query_pattern
```python
def query_pattern(self, pattern_type: str) -> Dict[str, Any]
```
Queries knowledge base for pattern information.

**Parameters:**
- `pattern_type`: Type of pattern to query

**Returns:**
- Pattern data including examples and relationships

## URLSources

```python
from core.url_sources import URLSources, DocumentationURLCollector

url_sources = URLSources()
collector = DocumentationURLCollector()
```

### URLSources Methods

#### add_url
```python
def add_url(self, url: str, category: str)
```
Adds a URL to the specified category.

#### get_urls
```python
def get_urls(self, category: str = None) -> Set[str]
```
Gets URLs for a category or all URLs if no category specified.

### DocumentationURLCollector Methods

#### process_documentation_page
```python
async def process_documentation_page(self, url: str) -> Optional[ProjectResource]
```
Processes a documentation page to extract project information.

#### download_project
```python
async def download_project(self, project: ProjectResource) -> bool
```
Downloads and extracts a project.

## LLM Interface

```python
from core.llm_interface import VisionOSCodeGenerator

generator = VisionOSCodeGenerator()
```

### Methods

#### generate_code
```python
def generate_code(self, requirements: Dict[str, Any]) -> str
```
Generates code based on requirements using knowledge base.

**Parameters:**
- `requirements`: Dictionary of code generation requirements

**Returns:**
- Generated code as string

## Prompt Templates

```python
from core.prompt_templates import VisionOSPromptTemplate

template = VisionOSPromptTemplate()
```

### Methods

#### generate_component_prompt
```python
def generate_component_prompt(self, component: str, knowledge_base: VisionOSKnowledgeBase) -> str
```
Generates an LLM prompt with context from knowledge base.

**Parameters:**
- `component`: Component to generate prompt for
- `knowledge_base`: Knowledge base instance

**Returns:**
- Formatted prompt string with context 