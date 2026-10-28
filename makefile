VENV = .venv/Scripts/python.exe
PYTHON = C:\Users\Emilien\AppData\Local\Programs\Python\Python312\python.exe
FILENAME = main.py



all: run

clean:
	@echo "Cleaning up..."
	@echo "Removing virtual environment..."
	@-rmdir /s /q __pycache__
	@-rmdir /s /q .venv

build:
	@echo "Building the project..."
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv .venv
	@echo "Installing dependencies..."
	@$(VENV) -m pip install -r requirements.txt

run:
	@echo "Running the project..."
	@echo "Using virtual environment: $(VENV)"
	@echo "Running $(FILENAME)"
	@$(VENV) $(FILENAME)
