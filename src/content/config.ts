import { defineCollection, z } from 'astro:content';

const projects = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string().or(z.date()),
    description: z.string().optional(),
    images: z.array(
      z.object({
        image: z.string(), // a plain URL string
        caption: z.string().optional(),
      })
    ).optional(),
  }),
  extensions: ['.md', '.mdx'],
});

export const collections = { projects };