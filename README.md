# Ciel Kernel 🧠⚙️

A polyvalent "Operating System" designed to govern AI Coding Agents. It prevents hallucinations, forces strict architectural adherence, and turns conversational AI into a disciplined, execution-oriented software engineer.

With the **Intelligence Release (V0.2.x)**, Ciel now integrates Local LLM-driven Semantic Analysis (via Ollama) to automatically detect gaps between documented intentions and actual code reality.

## 🚀 Key Features

* **LLM-Powered Purpose Resolution:** Dynamically extracts the repository's semantic intent from documentation.
* **Intelligent Evidence Extraction:** Analyzes source code to extract actual implementation facts.
* **Semantic Implementation Gap Detection:** Uses AI to find contradictions, missing features, and technical debt between intention and reality.
* **Maturity Auditing:** Generates a structured cognitive diagnostic of the repository's readiness state.
* **Resilient Fallbacks:** Deterministic fallback mechanisms ensure Ciel keeps working even if the LLM is offline or returns malformed data.

## 🛠️ Usage

Install the Ciel Kernel CLI:

```bash
pip install -e .
```

Run a full cognitive diagnostic on any repository:

```bash
ciel analyze ./path/to/repo
```

Other granular commands:
* `ciel purpose "Make a web app"` - Resolves ambiguous intent into a concrete Purpose Object.
* `ciel sources ./repo` - Classifies source files into Roles (intention vs. reality).
* `ciel gap ./repo` - Detects implementation gaps.
* `ciel report ./repo --format markdown` - Generates a comprehensive markdown report.

## 📂 Core Structure

* `AGENTS.md`: The supreme mandate. Overrides the AI's default helpful/chatty personality with strict engineering discipline.
* `ciel/`: The core Python package powering the intelligent OS.
  * `cli/`: Command-line interface orchestration.
  * `skills/`: Execution and reasoning SOPs (e.g., Gap Detection, Maturity Audit).
  * `rag/`: Document retrieval and evidence extraction capabilities.
  * `inference/`: LLM adapters (currently supporting local Ollama).
