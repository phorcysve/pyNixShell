# myshell - Advanced Python Shell

A robust, feature-rich Unix-like shell implemented entirely in Python. `myshell` provides a powerful command-line environment with advanced parsing, job control, and expansion capabilities, all while remaining highly extensible.

## Features

- **Advanced Parsing Engine**: Full support for complex pipelines (`|`), redirections (`>`, `>>`, `<`, `2>`), and background execution (`&`).
- **Rich Expansion Support**:
  - **Variable Expansion**: `$VAR` and `${VAR}` for environment variables.
  - **Command Substitution**: `$(command)` for dynamic output integration.
  - **History Expansion**: Quick access with `!!` (last command), `!N` (Nth command), and `!prefix` (last command starting with prefix).
- **Interactive REPL**:
  - **Tab Completion**: Intelligent completion for both executable commands and local files.
  - **Command History**: Persistent history management across sessions.
  - **Customizable Prompt**: Dynamic prompt reflecting current directory, time, and Git status.
- **Built-in Commands**: Essential shell built-ins including `cd`, `alias`, `unalias`, `export`, `unset`, `help`, and `exit`.
- **Job Control**: Manage background processes with `jobs`, `fg`, `bg`, and `disown` (under development).
- **Scripting Mode**: Execute shell scripts directly by passing the script path as an argument.
- **Extensible Architecture**:
  - **Plugin System**: Add custom commands and hooks via the `plug/` directory.
  - **Themes**: Customize your shell experience with themes in `thm/`.
- **Modular & Monolithic**: Choose between the single-file `sh.py` implementation or the modular components (`parse.py`, `exec.py`, etc.).

## Installation

### Prerequisites

- Python 3.8 or higher.
- No external dependencies required (uses standard library).

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd MAIN
   ```

2. (Optional) Build with Docker:
   ```bash
   docker build -t myshell .
   docker run -it myshell
   ```

## Usage

### Interactive Mode

Launch the shell for interactive use:
```bash
python3 sh.py
```

### Script Mode

Run a shell script file:
```bash
python3 sh.py your_script.sh
```

## Project Structure

- `sh.py`: The core monolithic shell implementation.
- `parse.py`, `exec.py`, `built.py`, `comp.py`, `hist.py`, `jobs.py`, `cfg.py`, `util.py`: Modular shell components.
- `plug/`: Plugin system for extending shell functionality.
- `thm/`: Theme definitions for shell customization.
- `test/`: Comprehensive test suite for shell logic and features.
- `ux/`: User interface and entry point configurations.

## Development

### Running Tests

Execute the test suite using `pytest`:
```bash
./test.sh
```
Or directly:
```bash
pytest test/
```

### Contributing

Contributions are welcome! Please refer to [contrib.md](contrib.md) for guidelines and the [roadmap.md](roadmap.md) for planned features.

## License

This project is licensed under the terms found in the [license](license) file.
