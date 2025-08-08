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

## Development Setup

### Python Environment
- Python 3.12.8 is available on the system
- Project intends to use conda for environment management (not yet configured)
- pygame will be the primary game framework

### Commands (To be established)
```bash
# Environment setup (planned)
conda create -n starpython python=3.12 pygame
conda activate starpython

# Running the game (once main.py exists)
python main.py

# Testing (once tests are created)
pytest
```

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