import type React from "react"
import type { Metadata } from "next"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"
import { Analytics } from "@vercel/analytics/next"
import { Suspense } from "react"
import "./globals.css"

export const metadata: Metadata = {
  title: "AI Medusa - Intelligent Automation Platform",
  description:
    "AI-powered automation platform with browser control, multi-agent execution, and intelligent task processing using Gemini AI",
  generator: "AI Medusa",
  keywords: ["ai", "automation", "browser", "playwright", "gemini", "multi-agent"],
  authors: [{ name: "likhoncodes" }],
  creator: "likhoncodes",
  publisher: "AI Medusa",
  openGraph: {
    title: "AI Medusa - Intelligent Automation Platform",
    description: "AI-powered automation platform with browser control and multi-agent execution",
    url: "https://github.com/likhoncodes/ai-medusa",
    siteName: "AI Medusa",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "AI Medusa - Intelligent Automation Platform",
    description: "AI-powered automation platform with browser control and multi-agent execution",
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`font-sans ${GeistSans.variable} ${GeistMono.variable}`}>
        <Suspense fallback={null}>{children}</Suspense>
        <Analytics />
      </body>
    </html>
  )
}
