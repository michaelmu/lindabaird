import { defineCollection, z } from 'astro:content';

const projects = defineCollection({
  type: 'content',
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      date: z.string().or(z.date()),
      description: z.string().optional(),
      images: z
        .array(
          z.object({
            image: image(),
            caption: z.string().optional(),
          })
        )
        .optional(),
    }),
  extensions: ['.md', '.mdx'],
});

export const collections = { projects };