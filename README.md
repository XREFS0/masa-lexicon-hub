# MASA Lexicon Dictionary

Comprehensive lexical definitions, etymologies, synonyms, and antonyms query engine

## Technical Architecture

The application is architected with modular separation of concerns adhering to modern clean code standards:

- **Component Layering**: Isolated view layouts, state managers, and service controllers.
- **Defensive Engineering**: Robust input sanitization and exception management.
- **Modern Design Standards**: High-contrast dark-mode interface styled for optimal usability and visual polish.

## Preview

![Application Interface](screenshots/app_interface.png)

## Features

- Structured lexical lookup delivering part of speech, definitions, and usage examples.
- Synonym and antonym relationship discovery cards.
- Search history cache and favorite words bookmarking system.
- Offline dictionary database fallback ensuring continuous operability.

## Prerequisites

- Python 3.10 or higher
- Required packages:

```bash
pip install customtkinter pillow requests
```

## Execution

Launch the application via Python:

```bash
python "English Dictionary App Using Tkinter in Python/main.py"
```

## Project Structure

```
.
├── English Dictionary App Using Tkinter in Python
├── screenshots/
│   └── app_interface.png
├── .gitignore
├── LICENSE             # MIT License
└── README.md           # Developer documentation
```

## License

This project is licensed under the terms of the MIT License. Refer to the `LICENSE` file for details.
