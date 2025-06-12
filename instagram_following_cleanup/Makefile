.PHONY: setup install clean run help lint

# Default Python interpreter
PYTHON := python3

# Virtual environment directory
VENV := venv

# Help target - shows available commands
help:
	@echo "Instagram Following Cleanup - Available Commands:"
	@echo "================================================="
	@echo "setup    - Set up virtual environment and install dependencies"
	@echo "install  - Install/update dependencies"
	@echo "run      - Run the Instagram cleanup script"
	@echo "lint     - Run code linting (requires flake8)"
	@echo "clean    - Remove virtual environment and cache files"
	@echo "help     - Show this help message"
	@echo ""
	@echo "Quick start:"
	@echo "1. make setup"
	@echo "2. cp .env.example .env && edit .env"
	@echo "3. make run"

# Set up virtual environment and install dependencies
setup:
	@echo "Setting up virtual environment..."
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
	@echo "Setup complete! Next steps:"
	@echo "1. cp .env.example .env"
	@echo "2. Edit .env with your Instagram access token"
	@echo "3. make run"

# Install or update dependencies
install:
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

# Run the main script
run:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
	@if [ ! -f ".env" ]; then \
		echo ".env file not found. Copy .env.example to .env and add your token."; \
		exit 1; \
	fi
	@if [ -f "src/instagram_cleanup.py" ]; then \
		$(VENV)/bin/python src/instagram_cleanup.py; \
	else \
		$(VENV)/bin/python instagram_cleanup.py; \
	fi

# Run linting (optional - requires flake8)
lint:
	@if [ -f "$(VENV)/bin/flake8" ]; then \
		if [ -f "src/instagram_cleanup.py" ]; then \
			$(VENV)/bin/flake8 src/*.py; \
		else \
			$(VENV)/bin/flake8 *.py; \
		fi; \
	else \
		echo "flake8 not installed. Installing..."; \
		$(VENV)/bin/pip install flake8; \
		if [ -f "src/instagram_cleanup.py" ]; then \
			$(VENV)/bin/flake8 src/*.py; \
		else \
			$(VENV)/bin/flake8 *.py; \
		fi; \
	fi

# Clean up generated files
clean:
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf src/__pycache__
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	@echo "Cleanup complete!"
