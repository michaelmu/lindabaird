// astro.config.mjs
import { defineConfig } from 'astro/config';
import { astroImageTools } from "astro-imagetools";
import mdx from '@astrojs/mdx';

export default defineConfig({
  integrations: [astroImageTools, mdx()],
  output: 'static',
  // When deployed, the site will live under /interior_design/ on lindabaird.com
  // When deployed, the site will live under /interior_design/ on lindabaird.com
  base: process.env.NODE_ENV === 'production'
    ? '/interior_design/'
    : '/',
});