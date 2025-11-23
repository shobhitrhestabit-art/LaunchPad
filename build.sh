#!/bin/bash

TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
BUILD_NAME="build-$TIMESTAMP.tgz"

echo "Creating build artifact: $BUILD_NAME"
tar -czf "$BUILD_NAME" src/ config.json logs/ eslint.config.js .prettierrc package.json validate.sh

# Generate SHA checksum
sha256sum "$BUILD_NAME" > "$BUILD_NAME.sha256"

echo "✅ Build completed: $BUILD_NAME"
