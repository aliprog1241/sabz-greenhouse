import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sabz Greenhouse | خدمات و تجهیزات گلخانه‌ای",
  description: "نسخه اولیه پلتفرم خدمات تخصصی و تجهیزات گلخانه‌ای",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="fa" dir="rtl" className="h-full antialiased">
      <body className="min-h-full">{children}</body>
    </html>
  );
}
