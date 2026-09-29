#!/usr/bin/env bash
# Sync Meridian static site to S3 with Vite-style cache headers.
# Run from site/ after `python3 build.py` (hashed CSS/JS already emitted).
set -euo pipefail
SITE="$(cd "$(dirname "$0")" && pwd)"
BUCKET="${BUCKET:-meridian-studio-site-543052825935}"
REGION="${REGION:-us-west-2}"
S3="s3://${BUCKET}"

cd "$SITE"
python3 build.py

echo "Uploading hashed CSS (immutable)…"
aws s3 sync . "$S3" --region "$REGION" \
  --exclude "*" --include "css/styles.*.css" \
  --cache-control "public, max-age=31536000, immutable" \
  --content-type "text/css; charset=utf-8" \
  --metadata-directive REPLACE

echo "Uploading hashed JS (immutable)…"
aws s3 sync . "$S3" --region "$REGION" \
  --exclude "*" --include "js/main.*.js" \
  --cache-control "public, max-age=31536000, immutable" \
  --content-type "application/javascript; charset=utf-8" \
  --metadata-directive REPLACE

echo "Uploading HTML (no-cache)…"
aws s3 sync . "$S3" --region "$REGION" \
  --exclude "*" --include "*.html" --exclude "node_modules/*" \
  --cache-control "no-cache" \
  --content-type "text/html; charset=utf-8" \
  --metadata-directive REPLACE

echo "Uploading llms/robots/sitemap/md/svg…"
aws s3 sync . "$S3" --region "$REGION" \
  --exclude "*" \
  --include "*.txt" --include "*.xml" --include "*.md" --include "*.svg" \
  --exclude "README.md" --exclude "BUILD_NOTES.md" --exclude "node_modules/*" \
  --cache-control "public, max-age=3600" \
  --metadata-directive REPLACE

# Offerings moved from /services/<slug>/ to /<slug>/. Drop the old prefix.
echo "Removing legacy /services/ objects…"
aws s3 rm "$S3/services/" --region "$REGION" --recursive

# Do not publish unhashed source assets
aws s3 rm "$S3/css/styles.css" --region "$REGION" 2>/dev/null || true
aws s3 rm "$S3/js/main.js" --region "$REGION" 2>/dev/null || true

# Prune stale hashed objects not present locally
for key in $(aws s3api list-objects-v2 --bucket "$BUCKET" --prefix "css/" --region "$REGION" \
  --query 'Contents[].Key' --output text 2>/dev/null); do
  base=$(basename "$key")
  [[ "$base" == styles.*.css ]] || continue
  [[ -f "css/$base" ]] || aws s3 rm "$S3/$key" --region "$REGION"
done
for key in $(aws s3api list-objects-v2 --bucket "$BUCKET" --prefix "js/" --region "$REGION" \
  --query 'Contents[].Key' --output text 2>/dev/null); do
  base=$(basename "$key")
  [[ "$base" == main.*.js ]] || continue
  [[ -f "js/$base" ]] || aws s3 rm "$S3/$key" --region "$REGION"
done

echo "Deployed to $S3 (region $REGION). Sync only — no extra AWS cost notes."
