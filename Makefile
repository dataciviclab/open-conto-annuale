PYTHON ?= python3
TOOLKIT = $(PYTHON) scripts/run_toolkit.py

# --- Anagrafica seeds ---

ANAG_SEEDS = \
	anagrafica/anag-enti \
	anagrafica/anag-comparti \
	anagrafica/anag-qualifiche \
	anagrafica/anag-voci-spesa \
	anagrafica/anag-causali \
	anagrafica/anag-territorio \
	anagrafica/anag-titoli-studio \
	anagrafica/anag-voci-fua \
	anagrafica/anag-fondi

DATASETS = \
	assenze \
	composizione-retribuzione \
	costo-lavoro \
	personale \
	anzianita \
	titoli-studio \
	comandati \
	contrattazione \
	flessibili \
	passaggi \
	distribuzione \
	retribuzione-media \
	modalita-flessibile \
	occupazione \n	occupazione
	oCCUPAZIONE \

# --- Download ZIP annuale (una tantum) ---

YEARS ?= 2024

.PHONY: download
download:
	@for y in $(YEARS); do \
		echo "=== Scarico $$y ==="; \
		python3 scripts/download_zip.py $$y; \
	done

# --- Estrazione dati ---

.PHONY: extract-dati
extract-dati:
	@for y in $(YEARS); do \
		zip="$$y""Tutto.zip"; \
		test -f "$$zip" || { echo "❌ $$zip mancante: fai 'make download'"; exit 1; }; \
		echo "=== Estrazione $$y ==="; \
		mkdir -p "_local/seed/dati/$$y"; \
		unzip -j -o "$$zip" "*$${y}Dati/*" -d "_local/seed/dati/$$y/" 2>&1 | tail -1; \
	done
	@echo "✅ Dati estratti in _local/seed/dati/{year}/"

# --- Seeds ---

.PHONY: seeds
seeds:
	@for d in $(ANAG_SEEDS); do \
		echo "=== $$d ==="; \
		$(TOOLKIT) run all --config $$d/dataset.yml || exit 1; \
	done

# --- Dataset ---

define run_dataset
.PHONY: run-$(1)
run-$(1): extract-dati
	$(TOOLKIT) run all --config $(1)/dataset.yml
endef

$(foreach ds,$(DATASETS),$(eval $(call run_dataset,$(ds))))

.PHONY: run-all
run-all: seeds
	@for d in $(DATASETS); do \
		echo "=== $$d ==="; \
		$(TOOLKIT) run all --config $$d/dataset.yml || exit 1; \
	done

# --- Smoke test ---

.PHONY: smoke-seeds smoke
smoke-seeds:
	@for d in $(ANAG_SEEDS); do \
		echo "=== $$d (smoke) ==="; \
		$(TOOLKIT) run all --config $$d/dataset.yml --sample-rows 1000 || exit 1; \
	done

smoke: smoke-seeds
	@for d in $(DATASETS); do \
		echo "=== $$d (smoke) ==="; \
		$(TOOLKIT) run all --config $$d/dataset.yml --year 2024 --sample-rows 1000 || exit 1; \
	done

# --- Validazione config ---

.PHONY: check
check:
	@for f in $$(find . -path '*/anagrafica/*' -name dataset.yml | sort); do \
		echo "→ $$f"; \
		$(TOOLKIT) inspect paths --config "$$f" --year 2024 > /dev/null 2>&1 || exit 1; \
	done
	@for d in $(DATASETS); do \
		echo "→ $$d/dataset.yml"; \
		$(TOOLKIT) inspect paths --config "$$d/dataset.yml" --year 2024 > /dev/null 2>&1 || exit 1; \
	done
	@echo "✅ All configs valid"

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
