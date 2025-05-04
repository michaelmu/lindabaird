// astro.config.mjs
import { defineConfig } from 'astro/config';
import { astroImageTools } from "astro-imagetools";
import mdx from '@astrojs/mdx';

export default defineConfig({
  integrations: [astroImageTools, mdx()],
  output: 'static',
  // When deployed, the site will live under /design/ on lindabaird.com
  // All assets are served from the root; use default base '/'
  base: '/',
});