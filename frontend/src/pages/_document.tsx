import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <meta charSet="utf-8" />
        <meta name="description" content="Tech news dashboard with 3D globe." />
        <meta name="theme-color" content="#050810" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
