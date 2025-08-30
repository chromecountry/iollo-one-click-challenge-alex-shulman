# One‑Click Deployment Challenge (2 hour time limit)

## Goal
Build a working prototype of a one‑click deployment system that can provision infrastructure for new customers. The system should include a sample data analysis capability to showcase what deployed instances can do. You'll need coding agents (Claude Code, Cursor, Copilot, etc.) to complete this in time.

## What you will build
- Infrastructure automation that includes:
    - Terraform modules for core resources (networking, compute, DNS)
    - CI/CD pipeline for deployment
    - One‑click deployment trigger (CLI or API)
    - DNS and SSL automation scripts
    - Local testing environment for on‑premise deployments
    - Simple data analysis pipeline with reporting

## Deliverables (GitHub repo)
- Repository name: `iollo-one-click-challenge-<your-name>`
- Include these at repo root:
    - `README.md`: quickstart with copy‑paste run commands + brief "Coding Agent Usage" section
    - `.github/workflows/deploy.yml`: CI that executes your flow
    - `infra/` with Terraform skeleton and variables
    - `scripts/` with automation (bash or powershell)
    - `cli/` or `api/` implementing the one‑click trigger
    - `onprem/` with kind/k3d stub and config
    - `automation/` with scripts or Makefile that coordinate the deployment flow
    - `analysis/` with modular components, data, outputs, and coordinator

## Scope and acceptance criteria

### Terraform
- Provide module folders for `networking`, `compute`, and `dns` under `infra/modules/`
- Provide an example `infra/envs/dev/` stack that wires modules together
- `terraform fmt` and `terraform validate` succeed locally
- Use variables for customer_id, region, and size (small/medium/large)

### Pipeline (GitHub Actions)
- Workflow runs on push to `main` and on dispatch
- Jobs: `validate`, `plan` (mock), `deploy` (dry), `test`
- `validate`: checks Terraform formatting and validation
- `plan`: uses a plan step with 
  `terraform plan -var="customer_id=${{ github.run_id }}" -lock=false`
- `deploy`: echoes dry‑run steps calling your `scripts/deploy_infrastructure.sh`
- `test`: runs `scripts/run_smoke_checks.sh` to verify all components exist and prints mock access URLs

### One‑click trigger
- Choose one: `cli/deploy-customer.sh` or `api/server.(ts|py|go)`
- Accept flags or JSON for customer name, region, and size
- Trigger the GitHub Actions workflow via API (use GitHub CLI or curl) or provide clear instructions

### DNS/SSL stubs
- Include a stubbed script `scripts/configure_dns.sh` showing steps to create a hosted zone/record and request an ACM cert
- Echo commands and placeholders; keep idempotency via safe checks

### On‑prem stub
- Provide `onprem/bootstrap.sh` that creates a local cluster with kind or k3d and prints a kubeconfig path
- Include a short `onprem/README.md` explaining how this maps to customer isolation

### Security and config
- Keep secrets in environment variables; include `.env.example`
- Parameterize customer‑specific inputs via variables

### Automation & Coordination
- Create scripts that automate the end-to-end deployment process
- Provide a single command that runs all necessary steps in sequence

### Data Analysis Pipeline (orchestrate multiple LLM agents with different roles)
- Build a modular analysis system where different LLM agents handle specific tasks:
    - Data processor: Loads and validates CSV data (100-500 rows)
    - Statistician: Computes descriptive stats, correlations, and identifies patterns
    - Visualizer: Creates appropriate charts based on the data characteristics
    - Report writer: Synthesizes findings into executive-ready insights
- Design it so each component can work independently but also pass results between them
- Include a coordinator script that runs the full pipeline (e.g., `make analyze`)
- Each component should save its outputs (files/JSON) for the next stage to use

## Requirements
- Include a "Coding Agent Usage" section in your README with 3-5 key prompts that accelerated your work

## Time guidance
- ~45 min: Terraform modules
- ~30 min: CI/CD pipeline and deployment trigger
- ~30 min: Analysis pipeline (data → stats → viz → report)
- ~15 min: Documentation and cleanup

## What we're looking for
- Working Terraform that validates
- CI/CD pipeline that runs successfully
- One-click deployment that actually triggers the pipeline
- Clear documentation and runnable commands

## Submission
- Push to a GitHub repo (private - just add daniollo as a collaborator) and share the URL
- Include example commands:
    - `make demo` or `./cli/deploy-customer.sh --customer acme --region us-east-1 --size small`
    - `gh workflow run deploy.yml -f customer=acme` (or curl for workflow_dispatch)

## Clarifications
- **LLM agents**: Use Claude for the analysis pipeline agents (API key provided in our email). Set it as ANTHROPIC_API_KEY
- **Infrastructure**: Keep it dry-run/mock - validation is what matters, not actual provisioning
- **State management**: Local state is fine for this challenge
- **Data**: Generate synthetic data or use any public CSV (health, financial - your choice)
- **Size variations**: Just change instance types and counts in your Terraform variables
- **Output format**: Markdown reports are perfect
- **Authentication**: Document the GitHub token requirement in your README

## Tips
- Start with the Terraform modules first - get them to validate before moving on
- Use coding agents aggressively - they can generate entire module structures
- Keep the deployment pipeline simple - dry runs are fine
- The analysis component can use any public dataset or generate synthetic data
- For the analysis pipeline, consider building LLM agents with different personas (e.g., "You are a data scientist" for the statistics component)