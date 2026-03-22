const { build } = require('vite');
const path = require('path');

async function main() {
  console.log('Starting build...');
  try {
    await build({
      configFile: path.resolve(__dirname, 'vite.config.ts'),
      mode: 'production',
      build: {
        outDir: path.resolve(__dirname, 'dist')
      }
    });
    console.log('Build completed!');
  } catch (e) {
    console.error('Build failed:', e);
  }
}

main();
