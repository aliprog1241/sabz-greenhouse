"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

const links = [
  ["/", "خانه"], ["/services", "خدمات تخصصی"], ["/products", "کاتالوگ محصولات"],
  ["/projects", "پروژه‌ها"], ["/certificates", "مدارک و گواهی‌ها"],
  ["/about", "درباره مجموعه"], ["/contact", "تماس با ما"], ["/privacy", "حریم خصوصی"],
] as const;

function BrandLogo() {
  return <span className="flex items-center gap-4">
    <span className="grid h-16 w-16 place-items-center rounded-[1.35rem] bg-navy text-white shadow-lg shadow-navy/20" aria-hidden>
      <svg viewBox="0 0 64 64" className="h-11 w-11" fill="none">
        <path d="M32 52V25" stroke="currentColor" strokeWidth="4" strokeLinecap="round"/>
        <path d="M31 31C20 31 13 24 12 12c12 1 19 8 19 19Z" fill="#45A779"/>
        <path d="M33 39c11 0 18-7 19-19-12 1-19 8-19 19Z" fill="#77C6A0"/>
        <path d="M20 52h24" stroke="#70A9D2" strokeWidth="4" strokeLinecap="round"/>
      </svg>
    </span>
    <span><span className="block text-2xl font-black text-navy">سبز گلخانه</span><span className="mt-1 block text-sm text-ink/50">خدمات و تجهیزات تخصصی</span></span>
  </span>;
}

export function SiteHeader() {
  const [open, setOpen] = useState(false);
  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    const close = (event: KeyboardEvent) => event.key === "Escape" && setOpen(false);
    window.addEventListener("keydown", close);
    return () => { document.body.style.overflow = ""; window.removeEventListener("keydown", close); };
  }, [open]);

  return <>
    <header className="sticky top-0 z-40 border-b border-navy/10 bg-paper/90 backdrop-blur-xl">
      <div className="shell flex min-h-28 items-center justify-between gap-6">
        <Link href="/" aria-label="صفحه اصلی سبز گلخانه"><BrandLogo /></Link>
        <button type="button" onClick={() => setOpen(true)} aria-expanded={open} aria-controls="side-menu" aria-label="باز کردن منوی اصلی" className="group grid h-14 w-14 place-items-center rounded-2xl border border-navy/15 bg-white text-navy shadow-sm transition hover:border-leaf hover:text-leaf">
          <span className="flex w-6 flex-col gap-1.5" aria-hidden><span className="h-0.5 w-full rounded bg-current"/><span className="h-0.5 w-4 self-end rounded bg-current transition group-hover:w-full"/><span className="h-0.5 w-full rounded bg-current"/></span>
        </button>
      </div>
    </header>
    <div className={`fixed inset-0 z-[60] transition ${open ? "pointer-events-auto" : "pointer-events-none"}`} aria-hidden={!open}>
      <button aria-label="بستن منو" onClick={() => setOpen(false)} className={`absolute inset-0 bg-navy/65 backdrop-blur-sm transition-opacity ${open ? "opacity-100" : "opacity-0"}`}/>
      <aside id="side-menu" role="dialog" aria-modal="true" aria-label="منوی اصلی" className={`absolute right-0 top-0 flex h-full w-[min(88vw,380px)] flex-col bg-navy p-7 text-white shadow-2xl transition-transform duration-300 ${open ? "translate-x-0" : "translate-x-full"}`}>
        <div className="flex items-center justify-between"><p className="text-2xl font-black">منوی اصلی</p><button onClick={() => setOpen(false)} aria-label="بستن منو" className="grid h-11 w-11 place-items-center rounded-full border border-white/20 text-2xl">×</button></div>
        <nav className="mt-10 flex flex-col" aria-label="ناوبری اصلی">{links.map(([href,label],index)=><Link onClick={() => setOpen(false)} key={href} href={href} className="flex items-center justify-between border-b border-white/10 py-4 text-lg text-white/80 transition hover:pr-2 hover:text-white"><span>{label}</span><span className="text-sm text-sky">۰{index+1}</span></Link>)}</nav>
        <Link onClick={() => setOpen(false)} href="/consultation" className="mt-auto rounded-2xl bg-leaf px-5 py-4 text-center text-lg font-black text-white">درخواست مشاوره</Link>
      </aside>
    </div>
  </>;
}
