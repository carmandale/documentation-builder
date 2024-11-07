# Core Functionality Tracker

## 1. URL Discovery and Processing ✅
- **get_documentation_links()** ✅
  - Successfully finds and categorizes URLs
  - Uses Playwright for dynamic content
  - Uses BeautifulSoup for static parsing
  - Categories: documentation, videos, other

- **analyze_documentation_structure()** ✅
  - Successfully analyzes page structure
  - Finds sections, topics, and samples
  - Uses BeautifulSoup for static analysis

## 2. Sample Detection and Processing ✅
- **process_documentation_page()** ✅
  - Uses Playwright selectors for dynamic content
  - Successfully finds downloadable samples
  - Returns ProjectResource with title, URL, and download info

- **download_project()** ✅
  - Successfully downloads projects
  - Creates sanitized directory names
  - Handles zip file extraction

## 3. Critical Patterns (DO NOT BREAK)
- **Dynamic Content Handling**
  ```python
  # Use Playwright for dynamic content
  title_elem = await page.query_selector('h1')
  title = await title_elem.text_content()
  
  # Use BeautifulSoup for static parsing
  soup = BeautifulSoup(content, 'html.parser')
  ```

- **Sample Processing Flow**
  1. Discover URLs ✅
  2. Process pages for samples ✅
  3. Download if needed ✅
  4. Analyze patterns ❌

## 4. Areas Needing Work
- **Cache System** ❌
  - Cache validation not working
  - Cache not being used effectively
  - Need to implement proper cache checks

- **Pattern Analysis** ❌
  - Results not displaying
  - Validation not complete
  - Need to fix pattern detection

- **Test Mode** ⚠️
  - Working but needs refinement
  - Using first 3 samples
  - Need better sample selection

## 5. Development Rules
1. **Preserve Working Code**
   - Never modify working core functionality
   - Add new features alongside existing ones
   - Test thoroughly before merging changes

2. **Content Processing**
   - Use Playwright for dynamic content
   - Use BeautifulSoup for static parsing
   - Maintain this separation strictly

3. **Error Handling**
   - Log all errors with context
   - Provide fallbacks where possible
   - Never break the processing chain

## 6. Current Focus
1. Fix pattern analysis display
2. Implement proper cache validation
3. Improve test mode sample selection
4. Add relationship tracking

## 7. Testing Requirements
- Run verify.sh before changes
- Test with both cache enabled/disabled
- Verify sample downloads work
- Check pattern analysis results 