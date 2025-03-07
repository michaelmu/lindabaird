// astro.config.mjs
import { defineConfig } from 'astro/config';
import { astroImageTools } from "astro-imagetools";
import mdx from '@astrojs/mdx';

export default defineConfig({
  integrations: [astroImageTools, mdx()], // ✅ Ensure MDX is properly integrated
  output: 'static',
  base: '/lj-collective-site/',
});