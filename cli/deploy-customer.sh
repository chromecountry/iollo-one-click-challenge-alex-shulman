#!/bin/bash
set -euo pipefail

# One-click deployment trigger CLI
# Triggers GitHub Actions workflow for customer deployment

# Default values
CUSTOMER=""
REGION="us-east-1"
SIZE="small"
REPO=""

# Usage function
show_usage() {
    cat << EOF
Usage: $0 --customer <name> [--region <region>] [--size <size>] [--repo <owner/repo>]

Deploy infrastructure for a new customer using GitHub Actions workflow.

Required:
  --customer <name>     Customer name/ID (required)

Optional:
  --region <region>     AWS region (default: us-east-1)
  --size <size>         Deployment size: small|medium|large (default: small)
  --repo <owner/repo>   GitHub repository (auto-detected if not provided)
  --help               Show this help message

Environment:
  GITHUB_TOKEN         GitHub personal access token (required)

Examples:
  $0 --customer acme
  $0 --customer acme --region eu-west-1 --size large
  $0 --customer startup-co --region ap-southeast-1 --size medium

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --customer)
            CUSTOMER="$2"
            shift 2
            ;;
        --region)
            REGION="$2"
            shift 2
            ;;
        --size)
            SIZE="$2"
            shift 2
            ;;
        --repo)
            REPO="$2"
            shift 2
            ;;
        --help|-h)
            show_usage
            exit 0
            ;;
        *)
            echo "Error: Unknown option $1" >&2
            show_usage >&2
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$CUSTOMER" ]]; then
    echo "Error: --customer is required" >&2
    show_usage >&2
    exit 1
fi

# Validate size parameter
if [[ "$SIZE" != "small" && "$SIZE" != "medium" && "$SIZE" != "large" ]]; then
    echo "Error: --size must be one of: small, medium, large" >&2
    exit 1
fi

# Load .env file if it exists and GITHUB_TOKEN is not set
if [[ -z "${GITHUB_TOKEN:-}" && -f .env ]]; then
    echo "Loading environment from .env file..." >&2
    set -a  # automatically export variables
    source .env
    set +a
fi

# GITHUB_TOKEN is now loaded and validated

# Validate GITHUB_TOKEN environment variable
if [[ -z "${GITHUB_TOKEN:-}" ]]; then
    echo "Error: GITHUB_TOKEN environment variable is required" >&2
    echo "Please set your GitHub personal access token:" >&2
    echo "  export GITHUB_TOKEN=your_token_here" >&2
    echo "Or create a .env file with GITHUB_TOKEN=your_token_here" >&2
    exit 1
fi

# Auto-detect repository if not provided
if [[ -z "$REPO" ]]; then
    if command -v gh &> /dev/null; then
        REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "")
    fi
    
    if [[ -z "$REPO" ]] && [[ -d .git ]]; then
        # Fallback: extract from git remote
        REPO=$(git remote get-url origin 2>/dev/null | sed -n 's#.*github\.com[:/]\([^/]*\)/\([^.]*\).*#\1/\2#p' || echo "")
    fi
    
    if [[ -z "$REPO" ]]; then
        echo "Error: Could not auto-detect repository. Please specify --repo owner/repo" >&2
        exit 1
    fi
fi

echo "🚀 One-Click Deployment Trigger"
echo "   Customer: $CUSTOMER"
echo "   Region: $REGION" 
echo "   Size: $SIZE"
echo "   Repository: $REPO"
echo ""

# Try GitHub CLI first (preferred method)
if command -v gh &> /dev/null; then
    echo "Using GitHub CLI to trigger workflow..."
    
    # Trigger the workflow
    if gh workflow run deploy.yml \
        -f customer="$CUSTOMER" \
        -f region="$REGION" \
        -f size="$SIZE" \
        --repo "$REPO"; then
        
        echo "✅ Successfully triggered deployment workflow!"
        echo ""
        echo "📋 Deployment Details:"
        echo "   • Customer ID: $CUSTOMER"
        echo "   • Region: $REGION"
        echo "   • Size: $SIZE"
        echo "   • Repository: $REPO"
        echo ""
        echo "🔍 Monitor progress:"
        echo "   gh run list --repo $REPO"
        echo "   gh run watch --repo $REPO"
        echo ""
        echo "🌐 Once deployed, your application will be available at:"
        echo "   https://app.$CUSTOMER.example.com"
        
    else
        echo "❌ Failed to trigger workflow via GitHub CLI" >&2
        exit 1
    fi
    
else
    # Fallback to curl with GitHub API
    echo "GitHub CLI not found. Using curl with GitHub API..."
    
    API_URL="https://api.github.com/repos/$REPO/actions/workflows/deploy.yml/dispatches"
    
    # Prepare JSON payload
    JSON_PAYLOAD='{"ref":"main","inputs":{"customer":"'$CUSTOMER'","region":"'$REGION'","size":"'$SIZE'"}}'
    
    # Make API request
    HTTP_STATUS=$(curl -s -w "%{http_code}" -o /tmp/gh_response.json \
        -X POST \
        -H "Accept: application/vnd.github.v3+json" \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$JSON_PAYLOAD" \
        "$API_URL")
    
    if [[ "$HTTP_STATUS" == "204" ]]; then
        echo "✅ Successfully triggered deployment workflow!"
        echo ""
        echo "📋 Deployment Details:"
        echo "   • Customer ID: $CUSTOMER"
        echo "   • Region: $REGION"
        echo "   • Size: $SIZE" 
        echo "   • Repository: $REPO"
        echo ""
        echo "🔍 Monitor progress at:"
        echo "   https://github.com/$REPO/actions"
        echo ""
        echo "🌐 Once deployed, your application will be available at:"
        echo "   https://app.$CUSTOMER.example.com"
        
    else
        echo "❌ Failed to trigger workflow. HTTP status: $HTTP_STATUS" >&2
        if [[ -f /tmp/gh_response.json ]]; then
            echo "Response:" >&2
            cat /tmp/gh_response.json >&2
            rm -f /tmp/gh_response.json
        fi
        exit 1
    fi
fi

echo ""
echo "🎉 Deployment triggered for $CUSTOMER ($REGION, $SIZE)"
