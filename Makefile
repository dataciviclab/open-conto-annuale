PYTHON ?= python3
TOOLKIT = toolkit

# --- Support seeds (anagrafiche) ---

SUPPORT_SEEDS = \
	support/anag-enti \
	support/anag-comparti \
	support/anag-qualifiche \
	support/anag-voci-spesa \
	support/anag-causali \
	support/anag-territorio \
	support/anag-titoli-studio \
	support/anag-voci-fua \
	support/anag-fondi

DATASETS = \
	datasets/assenze \
	datasets/composizione-retribuzione \
	datasets/costo-lavoro \
	datasets/personale \
	datasets/anzianita \
	datasets/titoli-studio \
	datasets/comandati \
	datasets/contrattazione \
	datasets/flessibili \
	datasets/passaggi \
	datasets/distribuzione \
	datasets/retribuzione-media \
	datasets/modalita-flessibile \
	datasets/occupazione

# --- Download + estrazione dati (unico script, 1 download per anno) ---

YEARS ?= 2024

.PHONY: extract-dati
extract-dati:
	python3 scripts/extract_dati.py $(YEARS)

# --- Seeds ---

.PHONY: seeds
seeds:
	@for d in $(SUPPORT_SEEDS); do \
		echo "=== $$d ==="; \
		$(TOOLKIT) run --config $$d/dataset.yml || exit 1; \
	done

# --- Dataset ---

# Pattern stile dcl-bologna: make run/<slug>
.PHONY: run/%
run/%: extract-dati
	$(TOOLKIT) run --config datasets/$*/dataset.yml

.PHONY: run-all
run-all: seeds
	@for d in $(DATASETS); do \
		echo "=== $$d ==="; \
		$(TOOLKIT) run --config $$d/dataset.yml || exit 1; \
	done

# --- Smoke test ---

.PHONY: smoke-seeds smoke
smoke-seeds:
	@for d in $(SUPPORT_SEEDS); do \
		echo "=== $$d (smoke) ==="; \
		$(TOOLKIT) run --config $$d/dataset.yml --sample-rows 1000 || exit 1; \
	done

smoke: smoke-seeds
	@for d in $(DATASETS); do \
		echo "=== $$d (smoke) ==="; \
		$(TOOLKIT) run --config $$d/dataset.yml --year 2024 --sample-rows 1000 || exit 1; \
	done

# --- Validazione config ---

.PHONY: check
check:
	@for f in $$(find . -path '*/support/*' -name dataset.yml | sort); do \
		echo "→ $$f"; \
		$(TOOLKIT) run preflight --config "$$f" --years 2024 > /dev/null 2>&1 || exit 1; \
	done
	@for d in $(DATASETS); do \
		echo "→ $$d/dataset.yml"; \
		$(TOOLKIT) run preflight --config "$$d/dataset.yml" --years 2024 > /dev/null 2>&1 || exit 1; \
	done
	@echo "✅ All configs valid"

# --- Registry ---

.PHONY: registry
registry:
	$(PYTHON) scripts/build_registry.py --write

# --- Pulizia ---

.PHONY: clean clean-runs
clean:
	rm -rf out/data/ .tmp/
clean-runs:
	rm -rf out/data/_runs/

# --- Verify ---

.PHONY: verify
verify:
	$(PYTHON) scripts/verify_output.py --all --year 2024

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:' Makefile | sort
