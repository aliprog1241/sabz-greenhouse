import type { Metadata } from "next";
import "./globals.css";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";

export const metadata: Metadata = { title:{default:"سبز گلخانه | خدمات و تجهیزات گلخانه‌ای",template:"%s | سبز گلخانه"}, description:"خدمات تخصصی، پروژه‌ها و کاتالوگ تجهیزات گلخانه‌ای برای سراسر ایران" };
export default function RootLayout({children}:{children:React.ReactNode}) { return <html lang="fa" dir="rtl" data-scroll-behavior="smooth"><body><SiteHeader />{children}<SiteFooter /></body></html>; }
