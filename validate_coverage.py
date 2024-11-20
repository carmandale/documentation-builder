#!/usr/bin/env python3
"""
Validate documentation coverage and generate a report.
"""

import asyncio
from pathlib import Path
import json
from datetime import datetime
from core.validation import DocumentationValidator
from core.config import REALITYKIT_SECTIONS
from utils.logging import logger

def convert_sets_to_lists(obj):
    """Convert any sets in the object to lists for JSON serialization."""
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {k: convert_sets_to_lists(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_sets_to_lists(item) for item in obj]
    return obj

async def main():
    try:
        # Initialize validator
        cache_dir = Path('data/cache')
        validator = DocumentationValidator(cache_dir)
        
        # Generate comprehensive report
        logger.info("Generating documentation coverage report...")
        report = validator.generate_coverage_report()
        
        # Convert any sets to lists for JSON serialization
        report = convert_sets_to_lists(report)
        
        # Save report
        report_file = cache_dir / f'coverage_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n=== Documentation Coverage Report ===\n")
        
        # Framework coverage
        print("Framework Coverage:")
        for section_name, coverage in report['coverage'].items():
            print(f"\n{section_name}:")
            print(f"  Main section: {'✅' if coverage['found'] else '❌'}")
            print(f"  Children found: {len(coverage['children_found'])}")
            print(f"  Children missing: {len(coverage['children_missing'])}")
            if coverage['issues']:
                print("  Issues:")
                for issue in coverage['issues']:
                    print(f"    - {issue}")
        
        # Statistics
        stats = report['statistics']
        print("\nOverall Statistics:")
        print(f"  Section Coverage: {stats['section_coverage_percentage']:.1f}%")
        print(f"  Child Coverage: {stats['child_coverage_percentage']:.1f}%")
        print(f"  Total Sections: {stats['total_sections']}")
        print(f"  Covered Sections: {stats['covered_sections']}")
        print(f"  Total Children: {stats['total_children']}")
        print(f"  Covered Children: {stats['covered_children']}")
        print(f"  Quality Issues: {stats['quality_issues']}")
        
        # Quality issues
        if 'quality' in report:
            quality = report['quality']
            if quality['code_examples']:
                print("\nCode Example Issues:")
                for doc, info in quality['code_examples'].items():
                    print(f"  {doc}: Found {info['found']}/{info['required']} examples")
            
            if quality['section_coverage']:
                print("\nMissing Sections:")
                for doc, info in quality['section_coverage'].items():
                    print(f"  {doc}: Missing {', '.join(info['missing_sections'])}")
            
            if quality['relationship_validation']:
                print("\nInvalid Relationships:")
                for doc, relationships in quality['relationship_validation'].items():
                    print(f"  {doc}: {len(relationships)} invalid relationships")
            
            if quality['broken_links']:
                print("\nBroken Links:")
                for link in quality['broken_links']:
                    print(f"  - {link}")
        
        print(f"\nDetailed report saved to: {report_file}")
        
    except Exception as e:
        logger.error(f"Error generating coverage report: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
