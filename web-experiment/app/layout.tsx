import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "WanderAI | Your Next-Gen AI Travel Agent",
  description: "Experience effortless travel planning with WanderAI's personalized, sustainable itineraries.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={cn(inter.className, "min-h-screen bg-slate-50 text-slate-900")}>
        <header className="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-slate-200">
          <nav className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <a href="/" className="text-2xl font-bold bg-gradient-to-r from-brand-600 to-brand-400 bg-clip-text text-transparent">
              WanderAI
            </a>
            <div className="flex gap-6 items-center">
              <a href="/demo" className="text-sm font-medium hover:text-brand-600 transition-colors">Demo</a>
              <a href="/faq" className="text-sm font-medium hover:text-brand-600 transition-colors">FAQ</a>
              <a href="/build" className="px-5 py-2 bg-slate-900 text-white rounded-xl text-sm font-bold hover:scale-[1.02] active:scale-95 transition-all">Start Planning</a>
            </div>
          </nav>
        </header>
        <main className="pt-16">
          {children}
        </main>
      </body>
    </html>
  );
}
