// astro.config.mjs
import { defineConfig } from 'astro/config';
import { astroImageTools } from "astro-imagetools";
import mdx from '@astrojs/mdx';

export default defineConfig({
  integrations: [astroImageTools, mdx()],
  output: 'static',
  base: process.env.NODE_ENV === 'production' ? '/lj-collective-site/' : '/',
});