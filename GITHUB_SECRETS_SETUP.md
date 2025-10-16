# GitHub Secrets Setup Guide

This guide explains how to configure GitHub Secrets for the CI/CD pipelines.

## Required Secrets

### 1. GITHUB_TOKEN (Automatically Provided)
- **Status**: ✅ No action needed
- **Purpose**: Used for authentication with GitHub API and GHCR (GitHub Container Registry)
- **Note**: This token is automatically provided by GitHub Actions and has the necessary permissions

## Optional Secrets

### 2. CODECOV_TOKEN (Optional)
- **Purpose**: Upload test coverage reports to Codecov
- **Status**: ⚠️ Optional - CI will pass without it
- **How to get**:
  1. Sign up at https://codecov.io with your GitHub account
  2. Add your repository
  3. Copy the upload token from repository settings
  4. Add to GitHub Secrets as `CODECOV_TOKEN`

### 3. Deployment Secrets (Future Use)

If you plan to deploy to external servers, you may need:

#### DEPLOY_SSH_KEY
- **Purpose**: SSH key for deployment to remote servers
- **Setup**:
  ```bash
  # Generate SSH key
  ssh-keygen -t ed25519 -C "github-actions@deploy" -f deploy_key

  # Add public key to server's ~/.ssh/authorized_keys
  # Add private key to GitHub Secrets as DEPLOY_SSH_KEY
  ```

#### DEPLOY_HOST
- **Purpose**: Deployment server hostname or IP
- **Example**: `staging.example.com` or `192.168.1.100`

#### DEPLOY_USER
- **Purpose**: SSH username for deployment
- **Example**: `deploy` or `ubuntu`

### 4. Monitoring & Notifications (Optional)

#### SENTRY_DSN
- **Purpose**: Error tracking with Sentry
- **How to get**: Create project at https://sentry.io

#### SLACK_WEBHOOK
- **Purpose**: Deployment notifications to Slack
- **How to get**: Create incoming webhook in Slack workspace

## How to Add Secrets to GitHub

### Via GitHub Web Interface

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Enter **Name** and **Value**
5. Click **Add secret**

### Via GitHub CLI

```bash
# Install GitHub CLI if not already installed
brew install gh

# Authenticate
gh auth login

# Add a secret
gh secret set SECRET_NAME --body "secret_value"

# Add a secret from file
gh secret set SECRET_NAME < secret_file.txt

# List all secrets
gh secret list
```

## Current CI/CD Status

### ✅ Working Without Additional Secrets

The current CI/CD pipelines will work with default GitHub tokens:

- **CI Pipeline** (`ci.yml`):
  - ✅ Multi-version testing (Python 3.8-3.11)
  - ✅ Code quality checks
  - ✅ Security scanning
  - ⚠️ Coverage reporting (optional, requires CODECOV_TOKEN)

- **CD Pipeline** (`deploy.yml`):
  - ✅ Docker image build and push to GHCR
  - ⚠️ Staging deployment (requires setup)
  - ⚠️ Production deployment (requires setup)

## Verification

To verify your secrets are set correctly:

1. **Check secret existence** (names only, values are hidden):
   ```bash
   gh secret list
   ```

2. **Test CI pipeline**:
   - Push a commit to `main` or `develop` branch
   - Check Actions tab for workflow status
   - Verify all jobs pass

3. **Test CD pipeline**:
   - Create and push a tag: `git tag v0.1.0 && git push origin v0.1.0`
   - Check Actions tab for deployment workflow
   - Verify Docker image is pushed to GHCR

## Troubleshooting

### CI Tests Failing
- Check if Neo4j service starts successfully
- Verify Python dependencies install correctly
- Review test logs in Actions tab

### Codecov Upload Failing
- Ensure `CODECOV_TOKEN` is set correctly
- Check if repository is added to Codecov
- Note: This is optional and won't fail the CI

### Docker Push Failing
- Verify `GITHUB_TOKEN` has `write:packages` permission
- Check if GHCR is enabled for your account
- Ensure you're using a supported branch or tag

## Security Best Practices

1. **Never commit secrets** to the repository
2. **Use repository secrets** for sensitive data
3. **Rotate secrets regularly** (every 90 days recommended)
4. **Use environment secrets** for different deployment stages
5. **Review secret access** in audit logs periodically

## Additional Resources

- [GitHub Actions Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GHCR Documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Codecov Documentation](https://docs.codecov.com/docs)
