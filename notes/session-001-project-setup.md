# Learning Session 001: Python Project Setup and Structure
Date: 2025-08-08

## Topics Covered

### 1. Environment Management with Conda

#### Understanding conda-forge
- **conda-forge** is a community-driven repository with 25,000+ packages (vs ~1,500 in Anaconda defaults)
- Acts like an "app store" for conda packages, solving the limitation of Anaconda's curated but limited default channel
- Key advantages:
  - Binary compatibility (all packages built with same compilers)
  - Handles system-level dependencies (e.g., SDL2 for pygame)
  - Cross-platform support (automatic builds for Windows, macOS, Linux)
  - More frequent updates than Anaconda defaults

#### Python Version Selection (Why 3.12 over 3.13)
- **Package ecosystem lag**: New Python versions take 6-12 months for full package support
- **Binary wheel availability**: Newer versions often lack pre-compiled packages
- **The "N-1 Rule"**: Use latest stable minus one for new projects
- Python 3.12 advantages:
  - Mature ecosystem (15+ months old)
  - Enhanced error messages with suggestions
  - Modern features (pattern matching, exception groups, type parameters)
  - Full pygame support

### 2. Python Project Structure Paradigms

#### Main Structure Patterns
1. **Flat/Simple Structure**: Good for scripts and learning
2. **Package Structure**: Most common for medium/large projects
3. **Src Layout**: Recommended by PyPA, ensures testing against installed version
4. **Application Structure**: Django/Flask style for web apps
5. **Game-Specific Structure**: Organized by game concepts (entities, scenes, systems)

#### Key Concepts Clarified

**Package Naming vs Directory Structure**
```
repository-name/          # Can use hyphens, capitals
├── src/                 # Optional organizational directory (NOT a package)
│   └── package_name/    # Must follow Python rules (lowercase, underscores)
│       └── __init__.py  # Makes it a package
```

**Entry Points**
- `__main__.py`: Executes with `python -m package_name`
- `main.py`: Just a regular module with no special meaning
- Don't need both - it's often redundant

**The __init__.py File**
- Makes a directory a Python package
- Controls public API with `__all__`
- Can contain initialization code
- Defines what gets imported with `from package import *`

### 3. Dependencies: environment.yml vs pyproject.toml

#### Different Purposes
- **environment.yml**: Manages Python interpreter and environment (conda's domain)
- **pyproject.toml**: Defines package metadata and dependencies (Python packaging)

#### Recommended Approach: Minimal Duplication
```yaml
# environment.yml - Minimal, delegates to pyproject.toml
name: starpython
channels:
  - conda-forge
dependencies:
  - python=3.12
  - pip
  - pip:
    - -e .  # Installs package using pyproject.toml dependencies
```

```toml
# pyproject.toml - Single source of truth for dependencies
[project]
name = "starpython"
dependencies = [
    "pygame>=2.5.0",
    "numpy>=1.24.0",
]
```

### 4. Neovim Diagnostics
- Underlined text indicates LSP diagnostics (errors, warnings, hints)
- Common keybindings to view messages:
  - `K` or `gl`: Show diagnostic float
  - `]d` / `[d`: Navigate between diagnostics
  - `:lua vim.diagnostic.open_float()`: Force show diagnostic

## Key Decisions Made

1. **Use Python 3.12** for stability and package ecosystem maturity
2. **Use conda with conda-forge channel** for better pygame support and system dependencies
3. **Package structure** with potential migration to src/ layout as project grows
4. **Minimal environment.yml** with dependencies in pyproject.toml to avoid duplication
5. **Use __main__.py** for entry point (not main.py) to support `python -m starpython`

## Important Learning Points

### The Mental Model
- **environment.yml**: "The workshop" (Python version, system tools)
- **pyproject.toml**: "The blueprint" (package definition, dependencies)
- **__init__.py**: "This is a package" marker
- **__main__.py**: "Run this when executed as a program"

### Best Practices Learned
1. Don't name your package "src" - it should have semantic meaning
2. Use the N-1 rule for Python versions in production projects
3. Prefer conda-forge over defaults channel for broader package availability
4. Use `pip install -e .` to bridge conda and pip dependency management
5. Keep single source of truth for dependencies (pyproject.toml when possible)

## Next Steps
- Create environment.yml with minimal configuration
- Set up pyproject.toml with game dependencies
- Establish initial package structure
- Begin implementing core game loop with pygame