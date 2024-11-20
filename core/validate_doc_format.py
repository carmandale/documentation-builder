import asyncio
import json
from pathlib import Path
import re
from typing import Dict, List, Any, Optional
from core.url_sources import DocumentationURLCollector
from core.config import MAX_CRAWL_DEPTH

# Documentation type definitions based on Apple's structure
DOC_TYPES = {
    'instance_method': {
        'patterns': ['func', 'method', 'instance method'],
        'required_fields': ['title', 'description', 'declaration', 'parameters'],
    },
    'class_method': {
        'patterns': ['class method', 'static method'],
        'required_fields': ['title', 'description', 'declaration'],
    },
    'property': {
        'patterns': ['property', 'instance property'],
        'required_fields': ['title', 'description', 'declaration'],
    },
    'protocol': {
        'patterns': ['protocol'],
        'required_fields': ['title', 'description', 'conformance'],
    },
    'class': {
        'patterns': ['class'],
        'required_fields': ['title', 'description', 'inheritance'],
    },
    'structure': {
        'patterns': ['struct', 'structure'],
        'required_fields': ['title', 'description', 'declaration'],
    },
    'enumeration': {
        'patterns': ['enum', 'enumeration'],
        'required_fields': ['title', 'description', 'cases'],
    },
    'framework': {
        'patterns': ['framework'],
        'required_fields': ['title', 'description', 'topics'],
    },
    'article': {
        'patterns': ['article', 'guide', 'documentation'],
        'required_fields': ['title', 'description'],
    }
}

def detect_doc_type(content: Dict[str, Any]) -> str:
    """Detect the type of documentation page based on content patterns."""
    
    # Check for method patterns
    if content.get('declaration'):
        decl = content['declaration'].get('swift', '').lower()
        if 'func' in decl:
            if 'static' in decl or 'class' in decl:
                return 'class_method'
            return 'instance_method'
        elif 'var' in decl or 'let' in decl:
            return 'property'
    
    # Check for type patterns
    if content.get('title'):
        title = content['title'].lower()
        if 'protocol' in title:
            return 'protocol'
        elif 'class' in title:
            return 'class'
        elif 'struct' in title:
            return 'structure'
        elif 'enum' in title:
            return 'enumeration'
    
    # Check for framework/article patterns
    if content.get('navigation_path'):
        if any('framework' in path.lower() for path in content['navigation_path']):
            return 'framework'
    
    # Default to article
    return 'article'

def create_semantic_chunks(text: str) -> List[str]:
    """Split text into semantic chunks based on sentence boundaries and length."""
    if not text:
        return []
    
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        if current_length + len(sentence) > 500:  # Max chunk size
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = len(sentence)
        else:
            current_chunk.append(sentence)
            current_length += len(sentence)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def validate_code_block(code_block: str) -> Dict[str, Any]:
    """Validate and analyze a code block."""
    analysis = {
        'language': 'unknown',
        'has_comments': False,
        'method_signatures': [],
        'imports': [],
        'length': len(code_block.split('\n'))
    }
    
    # Enhanced Swift detection
    swift_patterns = {
        'import': r'import\s+\w+',
        'func': r'func\s+\w+\s*(?:<[^>]+>)?\s*\([^)]*\)',
        'class': r'class\s+\w+(?::\s*\w+(?:\s*,\s*\w+)*)?',
        'struct': r'struct\s+\w+(?::\s*\w+(?:\s*,\s*\w+)*)?',
        'protocol': r'protocol\s+\w+(?::\s*\w+(?:\s*,\s*\w+)*)?',
        'property': r'(?:var|let)\s+\w+\s*:',
        'comment_line': r'\/\/.*$',
        'comment_block': r'\/\*[\s\S]*?\*\/',
    }
    
    # Detect Swift code
    for pattern_type, pattern in swift_patterns.items():
        matches = re.findall(pattern, code_block, re.MULTILINE)
        if matches:
            analysis['language'] = 'swift'
            if pattern_type == 'func':
                analysis['method_signatures'].extend(matches)
            elif pattern_type == 'import':
                analysis['imports'].extend(matches)
            elif pattern_type in ['comment_line', 'comment_block']:
                analysis['has_comments'] = True
    
    return analysis

def validate_doc_format(content: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the format of a documentation page."""
    validation_results = {}
    doc_type = detect_doc_type(content)
    
    # Validate title
    if 'title' in content:
        validation_results['title'] = {
            'status': 'valid',
            'length': len(content['title'])
        }
    else:
        validation_results['title'] = {
            'status': 'missing',
            'required': doc_type in DOC_TYPES
        }
    
    # Validate description
    if 'description' in content:
        chunks = create_semantic_chunks(content['description'])
        validation_results['description'] = {
            'status': 'valid',
            'length': len(content['description']),
            'chunks': len(chunks)
        }
    else:
        validation_results['description'] = {
            'status': 'missing',
            'required': doc_type in DOC_TYPES
        }
    
    # Validate declaration
    if 'declaration' in content:
        validation_results['declaration'] = {
            'status': 'valid',
            'swift': bool(content['declaration'].get('swift')),
            'formatted': bool(content['declaration'].get('formatted'))
        }
    else:
        validation_results['declaration'] = {
            'status': 'missing',
            'required': doc_type in ['instance_method', 'class_method', 'property']
        }
    
    # Validate parameters
    if 'parameters' in content:
        validation_results['parameters'] = {
            'status': 'valid',
            'count': len(content['parameters']),
            'complete': all('name' in p and 'description' in p for p in content['parameters'])
        }
    else:
        validation_results['parameters'] = {
            'status': 'missing',
            'required': doc_type in ['instance_method', 'class_method']
        }
    
    return validation_results

def generate_llm_summary(content: Dict[str, Any]) -> str:
    """Generate a concise summary suitable for LLM consumption."""
    doc_type = detect_doc_type(content)
    
    summary = []
    summary.append(f"Document Type: {doc_type}")
    
    if content.get('title'):
        summary.append(f"Title: {content['title']}")
    
    if content.get('description'):
        desc = content['description']
        if len(desc) > 100:
            desc = desc[:97] + '...'
        summary.append(f"Description: {desc}")
    
    if content.get('declaration'):
        decl = content['declaration'].get('swift', '')
        if len(decl) > 100:
            decl = decl[:97] + '...'
        summary.append(f"Declaration: {decl}")
    
    if content.get('parameters'):
        param_count = len(content['parameters'])
        summary.append(f"Parameters: {param_count} parameter(s)")
    
    return '\n'.join(summary)

def calculate_match_score(text: str, query: str) -> float:
    """Calculate a relevance score for a text match."""
    if not text or not isinstance(text, str):
        return 0.0
    
    text_lower = text.lower()
    query_lower = query.lower()
    
    # Exact match
    if text_lower == query_lower:
        return 10.0
    
    # Word boundary match (e.g. "system" as a whole word)
    words = text_lower.split()
    if query_lower in words:
        return 8.0
    
    # Start of word match (e.g. "system" at start of "systemUpdate")
    for word in words:
        if word.startswith(query_lower):
            return 6.0
    
    # Contains as substring
    if query_lower in text_lower:
        return 4.0
    
    return 0.0

def search_documentation(query: str, cache_dir: str = 'data/cache/documentation') -> List[Dict[str, Any]]:
    """Search through cached documentation for relevant content."""
    results = []
    cache_path = Path(cache_dir)
    
    if not cache_path.exists():
        print(f"Cache directory not found: {cache_dir}")
        return results
    
    for file_path in cache_path.glob('*.json'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    content = json.load(f)
                except json.JSONDecodeError:
                    # If JSON parsing fails, try reading as string
                    f.seek(0)
                    content_str = f.read().strip()
                    # Skip if empty or not valid content
                    if not content_str:
                        continue
                    content = {'title': file_path.stem, 'description': content_str}
                
            score = 0.0
            
            # Search in title
            if isinstance(content, dict):
                # Title match (highest weight)
                title = content.get('title', '')
                title_score = calculate_match_score(title, query)
                score += title_score * 1.5  # 50% boost for title matches
                
                # Description match
                desc = content.get('description', '')
                desc_score = calculate_match_score(desc, query)
                score += desc_score
                
                # Declaration match
                decl = content.get('declaration', {})
                if isinstance(decl, dict):
                    decl_text = decl.get('swift', '')
                    decl_score = calculate_match_score(decl_text, query)
                    score += decl_score * 1.2  # 20% boost for code matches
                
                # Topics/category match
                topics = content.get('topics', [])
                if isinstance(topics, list):
                    for topic in topics:
                        topic_score = calculate_match_score(str(topic), query)
                        score += topic_score * 0.8  # 20% penalty for topic matches
            else:
                # If content is not a dict, search in the raw content
                content_str = str(content)
                raw_score = calculate_match_score(content_str, query)
                score += raw_score * 0.5  # 50% penalty for raw content matches
                content = {'title': file_path.stem, 'description': content_str}
            
            if score > 0:
                results.append({
                    'file': file_path.name,
                    'score': round(score, 2),
                    'title': content.get('title', file_path.stem),
                    'description': content.get('description', '')[:200] + '...' if len(content.get('description', '')) > 200 else content.get('description', '')
                })
        
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            continue
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Print results
    for result in results[:5]:  # Show top 5 results
        print(f"\n- {result['file']} (score: {result['score']})")
        print(f"  Title: {result['title']}")
        print(f"  Description: {result['description']}")
        
    return results

async def validate_documentation(url: str):
    """Validate documentation format for a single page with enhanced analysis"""
    collector = DocumentationURLCollector()
    
    print(f"\nValidating documentation format for: {url}")
    print("-" * 60)
    
    await collector.cache_documentation_page(url)
    cache = collector._load_doc_content_cache()
    
    if not cache or 'pages' not in cache:
        print("❌ No documentation cached")
        return
        
    page_data = cache['pages'].get(url)
    if not page_data:
        print("❌ Target page not found in cache")
        return
    
    # Detect document type and get validation rules
    doc_type = detect_doc_type(page_data)
    type_info = DOC_TYPES.get(doc_type, {'required_fields': []})
    
    print(f"\nDetected Document Type: {doc_type}")
    print(f"Required Fields: {', '.join(type_info['required_fields'])}")
    
    # Common fields for all types
    common_fields = {
        'title': {'min_length': 2},
        'description': {'min_length': 10},
        'topics': {'required': False},
        'relationships': {'required': False},
        'see_also': {'required': False},
        'code_blocks': {'required': False},
    }
    
    print("\nValidation Results:")
    
    # Validate required fields for the specific type
    for field in type_info['required_fields']:
        content = page_data.get(field)
        if content:
            print(f"\n✅ {field}:")
            if isinstance(content, str):
                print(f"  Length: {len(content)} characters")
                if field == 'description':
                    chunks = create_semantic_chunks(content)
                    print(f"  Split into {len(chunks)} semantic chunks")
            elif isinstance(content, (list, dict)):
                print(f"  Contains {len(content)} items")
        else:
            print(f"\n❌ {field}: Missing required field for {doc_type}")
    
    # Validate common fields
    for field, rules in common_fields.items():
        if field not in type_info['required_fields']:  # Skip if already validated
            content = page_data.get(field)
            if content:
                print(f"\n✅ {field}:")
                if isinstance(content, str) and rules.get('min_length'):
                    if len(content) < rules['min_length']:
                        print(f"  ⚠️ Content length ({len(content)}) below minimum ({rules['min_length']})")
                    else:
                        print(f"  Length: {len(content)} characters")
            elif rules.get('required', False):
                print(f"\n❌ {field}: Missing required field")
            else:
                print(f"\nℹ️ {field}: Optional field not present")
    
    # Validate code blocks if present
    if page_data.get('code_blocks'):
        print("\nCode Blocks Analysis:")
        for i, block in enumerate(page_data['code_blocks']):
            analysis = validate_code_block(block)
            print(f"\nBlock {i+1}:")
            print(f"  Language: {analysis['language']}")
            print(f"  Length: {analysis['length']} lines")
            print(f"  Has comments: {analysis['has_comments']}")
            if analysis['method_signatures']:
                print(f"  Methods found: {len(analysis['method_signatures'])}")
                for sig in analysis['method_signatures'][:2]:  # Show first 2 signatures
                    print(f"    - {sig}")
            if analysis['imports']:
                print(f"  Imports: {', '.join(analysis['imports'])}")
    
    # Generate and display LLM-friendly summary
    print("\nLLM-Friendly Summary:")
    print("-" * 40)
    print(generate_llm_summary(page_data))

    # Validate documentation format
    validation_results = validate_doc_format(page_data)
    print("\nValidation Results:")
    for field, result in validation_results.items():
        print(f"\n{field}:")
        for key, value in result.items():
            print(f"  {key}: {value}")

def analyze_documentation_coverage():
    """Analyze the coverage and quality of cached documentation."""
    cache_path = Path('data/cache/documentation')
    if not cache_path.exists():
        print("Cache directory not found!")
        return
    
    stats = {
        'total_files': 0,
        'valid_json': 0,
        'with_title': 0,
        'with_description': 0,
        'with_code': 0,
        'with_topics': 0,
        'total_size': 0,
        'avg_description_length': 0,
        'file_types': {},
        'topic_frequency': {},
        'errors': []
    }
    
    descriptions = []
    
    for file_path in cache_path.glob('*.json'):
        stats['total_files'] += 1
        stats['total_size'] += file_path.stat().st_size
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    content = json.load(f)
                    stats['valid_json'] += 1
                    
                    if isinstance(content, dict):
                        if content.get('title'):
                            stats['with_title'] += 1
                        
                        desc = content.get('description', '')
                        if desc:
                            stats['with_description'] += 1
                            descriptions.append(len(desc))
                        
                        if content.get('declaration') or content.get('code_blocks'):
                            stats['with_code'] += 1
                        
                        topics = content.get('topics', [])
                        if topics:
                            stats['with_topics'] += 1
                            for topic in topics:
                                stats['topic_frequency'][topic] = stats['topic_frequency'].get(topic, 0) + 1
                        
                        doc_type = content.get('type', 'unknown')
                        stats['file_types'][doc_type] = stats['file_types'].get(doc_type, 0) + 1
                        
                except json.JSONDecodeError:
                    stats['errors'].append(f"JSON decode error in {file_path.name}")
        except Exception as e:
            stats['errors'].append(f"Error processing {file_path.name}: {str(e)}")
    
    if descriptions:
        stats['avg_description_length'] = sum(descriptions) / len(descriptions)
    
    print("\nDocumentation Analysis Results:")
    print("=" * 40)
    print(f"Total Files: {stats['total_files']}")
    print(f"Valid JSON: {stats['valid_json']} ({(stats['valid_json']/stats['total_files']*100 if stats['total_files'] else 0):.1f}%)")
    print(f"Files with Title: {stats['with_title']} ({(stats['with_title']/stats['total_files']*100 if stats['total_files'] else 0):.1f}%)")
    print(f"Files with Description: {stats['with_description']} ({(stats['with_description']/stats['total_files']*100 if stats['total_files'] else 0):.1f}%)")
    print(f"Files with Code: {stats['with_code']} ({(stats['with_code']/stats['total_files']*100 if stats['total_files'] else 0):.1f}%)")
    print(f"Files with Topics: {stats['with_topics']} ({(stats['with_topics']/stats['total_files']*100 if stats['total_files'] else 0):.1f}%)")
    print(f"Average Description Length: {stats['avg_description_length']:.1f} characters")
    print(f"Total Size: {stats['total_size']/1024/1024:.2f} MB")
    
    print("\nDocument Types:")
    for doc_type, count in sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {doc_type}: {count}")
    
    print("\nTop Topics:")
    for topic, count in sorted(stats['topic_frequency'].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {topic}: {count}")
    
    if stats['errors']:
        print("\nErrors encountered:")
        for error in stats['errors'][:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(stats['errors']) > 10:
            print(f"  ... and {len(stats['errors'])-10} more errors")
    
    return stats

if __name__ == "__main__":
    # Test with a method documentation page
    url = "https://developer.apple.com/documentation/realitykit/system/update(context:)"
    asyncio.run(validate_documentation(url))
    
    print("\nTesting search functionality:")
    print("----------------------------------------")
    
    search_terms = ['update', 'system']
    for term in search_terms:
        print(f"\nSearching for '{term}':")
        results = search_documentation(term)
    
    print("\nAnalyzing documentation coverage:")
    analyze_documentation_coverage()
