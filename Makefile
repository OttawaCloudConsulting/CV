.PHONY: build validate pdf all install

# Build CV.md from project JSON files
build:
	python3 scripts/build_cv.py

# Validate all project JSON files
validate:
	@failed=0; passed=0; \
	for f in assets/projects/project_*.json; do \
		[ "$$(basename $$f)" = "project_template.json" ] && continue; \
		if bash tests/validators/validate-projects.sh "$$f" --quiet >/dev/null 2>&1; then \
			passed=$$((passed+1)); \
		else \
			echo "FAIL: $$f"; \
			failed=$$((failed+1)); \
		fi; \
	done; \
	echo "Validation complete: $$passed passed, $$failed failed"; \
	exit $$failed

# Generate PDF from CV.md using Pandoc + XeLaTeX
pdf:
	pandoc CV.md -o assets/documents/Christian_Turner-CV.pdf \
		--pdf-engine=xelatex \
		--standalone \
		-V documentclass=article \
		-V classoption=oneside \
		-V geometry:margin=1in \
		-V papersize=letter \
		-V fontsize=11pt \
		-V mainfont="Helvetica Neue" \
		-V monofont="Menlo" \
		-V linestretch=1.15 \
		-V colorlinks=true \
		-V linkcolor=blue \
		--syntax-highlighting=tango \
		--toc --toc-depth=2

# Install Python dependencies
install:
	pip install -r requirements.txt

# Run full pipeline: validate → build → pdf
all: validate build pdf
