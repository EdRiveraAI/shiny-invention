import type {Metadata, Viewport} from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Welas Product Studio',
  description: 'A private workspace for planning, producing, and launching Welas Early Learning resources.',
  robots: {index: false, follow: false},
};

export const viewport: Viewport = {width: 'device-width', initialScale: 1};

export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
