import Link from "next/link";

export function PageHero({ eyebrow, title, description }: { eyebrow: string; title: string; description: string }) {
  return <section className="shell py-16 sm:py-24"><p className="eyebrow">{eyebrow}</p><h1 className="mt-5 max-w-4xl text-4xl font-black leading-[1.35] text-forest sm:text-6xl">{title}</h1><p className="mt-6 max-w-3xl text-lg leading-9 text-ink/65">{description}</p></section>;
}

export function EmptyState({ text = "هنوز محتوای منتشرشده‌ای وجود ندارد." }: { text?: string }) {
  return <div className="rounded-3xl border border-dashed border-forest/25 bg-white p-10 text-center text-ink/55">{text}</div>;
}

export function DemoBadge() { return <span className="rounded-full bg-gold/20 px-3 py-1 text-xs font-bold text-forest">DEMO آزمایشی</span>; }

export function ArrowLink({ href, children }: { href: string; children: React.ReactNode }) {
  return <Link href={href} className="inline-flex items-center gap-2 font-bold text-leaf hover:text-forest">{children}<span aria-hidden>←</span></Link>;
}
