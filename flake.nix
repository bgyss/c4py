{
  description = "c4py - A Python implementation of the C4 ID system";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        # Python with required packages
        python = pkgs.python312;
        pythonPackages = python.pkgs;
        
        # Development dependencies from pyproject.toml
        devDependencies = with pythonPackages; [
          # Core dependencies
          click
          
          # Development dependencies
          black
          flake8
          isort
          mkdocs-material
          # ty is not available in nixpkgs yet, will use uv to install
          pytest
          pytest-cov
          ruff
          tox
        ];

        # Build the c4py package
        c4py = pythonPackages.buildPythonPackage rec {
          pname = "c4py";
          version = "0.1.0";
          format = "pyproject";

          src = builtins.path { path = ./.; name = "c4py-source"; };

          nativeBuildInputs = with pythonPackages; [
            hatchling
          ];

          propagatedBuildInputs = with pythonPackages; [
            click
          ];

          # Don't run tests during build - they're handled separately in checks
          doCheck = false;

          pythonImportsCheck = [ "c4py" ];

          meta = with pkgs.lib; {
            description = "A Python implementation of the C4 ID system";
            homepage = "https://github.com/bgyss/c4py";
            license = licenses.mit;
            maintainers = [ ];
          };
        };

      in
      {
        # The default package
        packages = {
          default = c4py;
          c4py = c4py;
        };

        # Development shell
        devShells.default = pkgs.mkShell {
          buildInputs = [
            # Python and packages
            python
            pythonPackages.pip
            pythonPackages.setuptools
            pythonPackages.wheel
            pythonPackages.hatchling
            
            # UV for package management
            pkgs.uv
            
            # Git for version control
            pkgs.git
            pkgs.gh
            
            # Development tools
            pkgs.just  # Task runner
            pkgs.direnv  # Environment management
          ] ++ devDependencies;

          # Environment variables
          shellHook = ''
            echo "🐍 c4py development environment"
            echo "Python: $(python --version)"
            echo "UV: $(uv --version)"
            echo ""
            echo "Available commands:"
            echo "  uv sync --dev     - Install dependencies"
            echo "  pytest           - Run tests"
            echo "  ruff check .     - Run linting"
            echo "  ruff format .    - Format code"
            echo "  uv run ty check . - Type checking"
            echo "  c4py --help      - Run the CLI tool"
            echo ""
            
            # Only show setup instructions if .venv doesn't exist
            if [ ! -d ".venv" ]; then
              echo "⚠️  Virtual environment not found."
              echo "   Run: uv venv && source .venv/bin/activate && uv sync --dev"
              echo ""
            fi
          '';

          # Python environment
          PYTHONPATH = ".";
          
          # Prevent Python from creating __pycache__ directories
          PYTHONDONTWRITEBYTECODE = "1";
          
          # Unbuffered Python output
          PYTHONUNBUFFERED = "1";
        };

        # Applications that can be run with `nix run`
        apps = {
          default = {
            type = "app";
            program = "${c4py}/bin/c4py";
          };
          
          c4py = {
            type = "app";
            program = "${c4py}/bin/c4py";
          };
        };

        # Checks (run with `nix flake check`)
        checks = {
          # Run tests
          pytest = pkgs.runCommand "c4py-tests" {
            buildInputs = [ python ] ++ devDependencies;
          } ''
            cp -r ${builtins.path { path = ./.; name = "c4py-source"; }} source
            cd source
            chmod -R +w .
            pytest tests/
            touch $out
          '';

          # Linting
          ruff-check = pkgs.runCommand "c4py-ruff-check" {
            buildInputs = [ pythonPackages.ruff ];
          } ''
            cp -r ${builtins.path { path = ./.; name = "c4py-source"; }} source
            cd source
            chmod -R +w .
            export RUFF_CACHE_DIR=$(mktemp -d)
            ruff check .
            touch $out
          '';

          # Type checking with ty (using uv since ty not in nixpkgs)
          ty-check = pkgs.runCommand "c4py-ty-check" {
            buildInputs = [ python uv ] ++ devDependencies;
          } ''
            cp -r ${builtins.path { path = ./.; name = "c4py-source"; }} source
            cd source
            chmod -R +w .
            export UV_CACHE_DIR=$(mktemp -d)
            ${uv}/bin/uv sync --dev
            ${uv}/bin/uv run ty check .
            touch $out
          '';
        };
      }
    );
}