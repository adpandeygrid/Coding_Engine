# Railway Deployment - Build Packages During Docker Build

## Problem

Pushing `language-packages/` (4.5GB) to git is failing with HTTP 500 errors due to repository size limits.

## Solution: Build Packages During Docker Build

Instead of committing large packages, we'll build them during the Docker build process.

### Step 1: Use the Build-Time Dockerfile

I've created `Dockerfile.railway.build` that builds packages during the Docker build.

**Option A: Rename the build Dockerfile**
```bash
# Backup current Dockerfile
mv Dockerfile.railway Dockerfile.railway.backup

# Use the build-time version
mv Dockerfile.railway.build Dockerfile.railway
```

**Option B: Update railway.json to use the build Dockerfile**
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile.railway.build"
  }
}
```

### Step 2: Remove language-packages from Git

Since we're building during Docker build, we don't need packages in git:

```bash
# Remove from git (but keep locally)
git rm -r --cached language-packages/

# Add back to .gitignore
echo "language-packages" >> .gitignore

# Commit the changes
git add .gitignore
git commit -m "Remove packages from git, will build during Docker build"
```

### Step 3: Deploy to Railway

```bash
git push origin main
```

Railway will:
1. Build the Docker image
2. Install runtimes during build (takes ~30-45 minutes first time)
3. Deploy with all runtimes included

## Trade-offs

**Pros:**
- ✅ No need to commit 4.5GB to git
- ✅ Smaller repository
- ✅ No Git LFS needed
- ✅ Packages always match the build environment

**Cons:**
- ⚠️ First build takes 30-45 minutes (subsequent builds are faster with caching)
- ⚠️ Requires internet during build (to clone Piston repo)

## Alternative: Pre-built Docker Image

If build times are too long, you can:

1. **Build locally and push to Docker Hub:**
   ```bash
   docker build -f Dockerfile.railway.build -t yourusername/piston-with-runtimes:latest .
   docker push yourusername/piston-with-runtimes:latest
   ```

2. **Update Dockerfile.railway to use your image:**
   ```dockerfile
   FROM yourusername/piston-with-runtimes:latest
   # Packages already included, no build needed
   ```

3. **Update railway.json:**
   ```json
   {
     "build": {
       "builder": "DOCKERFILE",
       "dockerfilePath": "Dockerfile.railway"
     }
   }
   ```

This way, Railway just pulls your pre-built image (fast!) instead of building from scratch.

## Current Recommendation

**For Railway deployment, use `Dockerfile.railway.build`** - it builds packages during Docker build, avoiding the need to commit large files to git.

