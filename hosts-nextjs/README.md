## Welcome to the Website Design Portion of this workshop!

For this lab we are learning how to build in next.js so then the great backend the you constructed can be matched with a beautiful fronend design!

Now, before we start. I wanted to get something out of the way. This is a beginner lab so expect and understand the follow:

1. We are a building extremely simplistic frontend.
2. We have a focus on how to START a nextjs project more than usual.
3. This is an mcp server. Thats all it really is. This means that it can only get so pretty. The more functionaily you have, the more you can make is stylish and cool.
4. This lab is about how to start it, then learn what the file system usually looks. Then check out the code, and hopefully provided comments should clear up confusion.

With that being said. let's set this up.

We first need to install quite a few things

npm install next react react-dom
npm install -D tailwindcss postcss autoprefixer typescript @types/node @types/react @types/react-dom

What is this? well:
next -> Next.js Framework   react -> React library for making UI    react-dom -> Rendering React on the Browser
tailwindcss -> tailwindcss (OPTIONAL, will explain)     postcss -> processing CSS (needed for Tailwind)
autoprefixer -> compability between browser and CSS     typescript -> a superset of JavaScript (JavaScript+)
@types/*name* this will give typescript types to given *name*

START :: Personal Ramble :: START
Now I installed tailwind css for this. You don't. Tailwind is a modern and increasely used CSS framework to build
user interfaces. Now, I will give a PERSONAL opinion, if you want a classic website look, and you want it very fast
using bootstrap rather than tailwind would be not a terrible idea. I used it when I first started web design, and it
was very good at giving you a fast and simple demo. It is being used less and less as tailwind is generally better 
BUT maybe for a hackathon and being new to website design bootstrap ain't a bad idea.
END :: Personal Ramble :: END

Additionally, quick reminder. This lab we are mainly using MCPs to talk to AIs (in this case Ollama) to get infomation from an AI that Ollama has (the government weather API)

now I'll let the starting READme.md do some of the heavy lifting::

START :: starting READme.md guide :: START
This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server: (Do this in the folder where the code is. For me I did it in the host-nextjs)

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
END :: starting READme.md guide :: END

NOTE :: to have this work enter in
    ollama serve
this will start ollama.