#!/bin/bash
# Build script for Hugging Face deployment

echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Build complete! Frontend ready at frontend/dist/"
