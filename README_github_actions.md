Get Render Deploy Hook URL:
- Render Dashboard → the service → Settings
- "Deploy Hook"
- “Generate Deploy Hook”
- Copy the URL


Set up GitHub Secrets
Go to your GitHub repo → Settings → Secrets → Actions → Add:
```
Secret name	Value
DOCKER_USERNAME	Docker Hub username
DOCKER_PASSWORD	Docker Hub access token
RENDER_DEPLOY_HOOK_URL	Render deploy hook URL
```



In the project root folder (where the Dockerfile is), run:

```
mkdir -p .github/workflows
```

```
touch .github/workflows/deploy.yml
```

Commit and push the workflow

```
git add .github/workflows/deploy.yml

git commit -m "Add deploy workflow"

git push

```

You can now go to the Actions tab in your GitHub repository to watch the workflow run when you push to main.

# Test

- Update your project

- Push the change to main, wait for GitHub Actions to:
    - Build your image
    - Push it to Docker Hub
    - Trigger Render to redeploy