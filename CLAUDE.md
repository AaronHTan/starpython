# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a 2D space exploration game built with pygame, featuring procedurally generated terrain. The project is specifically designed for learning Python and honing software engineering practices.

## Learning Mode Instructions

**IMPORTANT**: This is a learning project. Unless the user explicitly says "override", DO NOT write code directly. Instead:
1. Explain the thought process behind each task
2. Describe what the code would do and why
3. Provide detailed explanations when answering questions
4. Guide through the reasoning and best practices

### Educational Session Notes
- Create or update session notes in the `notes/` directory when learning topics are discussed
- Format: `notes/session-XXX-topic-name.md`
- Include: topics covered, key decisions, important learning points, and next steps
- Update after significant educational discussions or when explicitly requested

## Development Setup

### Python Environment
- Python 3.12.8 is available on the system
- Uses conda with conda-forge channel for environment management
- pygame is the primary game framework
- Dependencies managed through pyproject.toml with minimal environment.yml

### Commands
```bash
# Environment setup
conda env create -f environment.yml
conda activate starpython

# Running the game
python -m starpython  # Executes __main__.py

# Testing (once tests are created)
pytest

# Development tools (when configured)
black .         # Code formatting
mypy .          # Type checking
flake8          # Linting
```

### Project Structure Decisions
- Package layout: `starpython/starpython/` containing the package
- Entry point: `__main__.py` (not main.py) for `python -m` execution
- Dependencies: Single source of truth in pyproject.toml
- Environment: Minimal environment.yml using `pip install -e .`

## Architecture Goals

### Planned Structure
The game will need the following core components:
- **Main Game Loop**: Handle pygame initialization, events, updates, and rendering
- **Player System**: Spacecraft control and physics
- **World Generation**: Procedural terrain generation algorithms
- **Exploration Mechanics**: Discovery and navigation systems

### Key Technical Considerations
- Use pygame's sprite system for game objects
- Implement procedural generation using noise algorithms (e.g., Perlin noise)
- Design with modularity in mind - separate game logic from rendering
- Consider performance optimization for large procedurally generated worlds

## Python Learning Focus Areas
- Object-oriented design patterns for game entities
- Event-driven programming with pygame
- Algorithm implementation for procedural generation
- Performance profiling and optimization
- Clean code principles and PEP 8 compliance