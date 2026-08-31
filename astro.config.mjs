import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://grokbot-zh.local',
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory' },
  devToolbar: { enabled: false },
  server: { host: true, port: 4380 },
});
