# Research Assistance Fallback Strategy for Scientific Proposals

## Overview

When assisting with scientific proposal writing and literature research, external literature search tools (Semantic Scholar, arXiv, OpenAlex) may fail due to rate limiting, timeouts, or API issues. This document outlines a fallback strategy that prioritizes project documentation when external searches are unavailable.

## Core Principle

**Project documentation first, external search second.**

When asked about specific methods, techniques, or concepts in a research project:

1. **First**: Check project documentation, notes, and existing materials
2. **Second**: Attempt external literature searches if needed
3. **Third**: Provide comprehensive overview based on available information

## Rationale

1. **Project documentation is often more detailed** than general literature
2. **Information is already curated** for the specific research context
3. **External searches may fail** due to rate limiting, timeouts, or missing API keys
4. **Project documentation is always available** and doesn't depend on external services

## Workflow Pattern

### Step 1: Check Project Documentation
```bash
# Search for relevant files in the project
find . -name "*.md" -exec grep -l "method_name\|concept" {} \;

# Read key documentation files
cat core.md | grep -A 10 -B 5 "method_name"
```

### Step 2: Extract Key Information
From project documentation, extract:
- Method description and parameters
- Implementation details
- Results and validation
- Comparison with other methods
- Timeline and progress

### Step 3: Provide Comprehensive Overview
Based on project documentation, provide:
- Technical details and specifications
- Results and achievements
- Differentiation from other methods
- Timeline and progress
- Role in the overall research

## Example: HalluDesign Method

When asked about "HalluDesign starting point and progress":

1. **First**: Searched project documentation using `grep -r "HalluDesign" --include="*.md"`
2. **Found**: Extensive documentation in core.md, PIPELINE.md, academic reports
3. **Extracted**: Method details, parameters, results, timeline
4. **Provided**: Comprehensive overview without needing external searches

## Benefits

1. **Reliability**: Project documentation is always available
2. **Relevance**: Information is already tailored to the specific research
3. **Efficiency**: No need to wait for API responses or handle rate limits
4. **Depth**: Project documentation often contains more detailed implementation specifics

## Limitations

1. **Scope**: Only covers methods and concepts documented in the project
2. **Currency**: May not include the very latest external developments
3. **Validation**: Information is project-specific, not general literature validation

## When to Use External Searches

Use external literature searches when:
- Project documentation is insufficient
- Need to validate claims against general literature
- Looking for latest developments not yet in project docs
- Need broader context beyond the specific project

## Integration with Proposal Writing

This fallback strategy is particularly useful for proposal writing because:
1. **Project documentation contains the exact methods** being proposed
2. **Results and validation are already available** in project files
3. **Comparisons with other methods** are often documented
4. **Timeline and progress** are tracked in project documentation

## Tool-Specific Notes

### Semantic Scholar API
- Rate limit: 1 request/second with API key
- Common failure: 429 Too Many Requests
- Fallback: Check project documentation first

### arXiv API
- Rate limit: 1 request every 3 seconds
- Common failure: Timeout errors
- Fallback: Check project documentation first

### OpenAlex API
- Rate limit: Varies by plan
- Common failure: Module dependency issues
- Fallback: Check project documentation first

## Best Practices

1. **Always check project documentation first** for project-specific methods
2. **Use external searches for validation** and broader context
3. **Document the source** of information (project docs vs external)
4. **Note limitations** when relying solely on project documentation
5. **Update project documentation** with new external findings when available