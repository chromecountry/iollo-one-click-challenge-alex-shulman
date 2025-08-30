.PHONY: demo analyze onprem clean help

# Default target
help:
	@echo "Available targets:"
	@echo "  demo     - Run demo deployment"
	@echo "  analyze  - Run analysis pipeline"
	@echo "  onprem   - Bootstrap on-premise cluster"
	@echo "  clean    - Clean up resources"
	@echo ""
	@echo "Environment variables:"
	@echo "  CUSTOMER - Customer name for onprem target"
	@echo ""
	@echo "Examples:"
	@echo "  make demo"
	@echo "  make onprem CUSTOMER=acme"
	@echo "  CUSTOMER=startup make onprem"

demo:
	@echo "🚀 Running demo deployment..."
	@../../../../cli/deploy-customer.sh --customer demo-customer --region us-east-1 --size small

analyze:
	@../analysis/run_analysis.sh

onprem:
	@if [ -z "$(CUSTOMER)" ]; then \
		echo "Error: CUSTOMER variable is required"; \
		echo "Usage: make onprem CUSTOMER=<name>"; \
		echo "   or: CUSTOMER=<name> make onprem"; \
		exit 1; \
	fi
	@echo "🏗️ Bootstrapping on-premise cluster for customer: $(CUSTOMER)"
	@../onprem/bootstrap.sh $(CUSTOMER)

clean:
	@echo "🧹 Cleaning up resources..."
	@echo "This would typically:"
	@echo "  1. Delete kind clusters"
	@echo "  2. Clean temporary files"
	@echo "  3. Reset local state"
	@echo ""
	@echo "Manual cleanup:"
	@echo "  kind get clusters | xargs -I {} kind delete cluster --name {}"
	@echo "  docker system prune -f"
