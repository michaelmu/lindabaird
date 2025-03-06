import { defineConfig } from 'astro/config';
import image from 'astro-imagetools';
import mdx from '@astrojs/mdx';

export default defineConfig({
  integrations: [image(), mdx()],
});