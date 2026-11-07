import Link from "next/link";

const links = [
  ["/", "خانه"], ["/services", "خدمات"], ["/products", "محصولات"],
  ["/projects", "پروژه‌ها"], ["/certificates", "مدارک"], ["/about", "درباره ما"],
] as const;

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-50 border-b border-ink/10 bg-paper/90 backdrop-blur-xl">
      <div className="shell flex min-h-20 items-center justify-between gap-6">
        <Link href="/" className="text-lg font-black text-forest">سبز گلخانه <span className="text-gold">•</span></Link>
        <nav aria-label="ناوبری اصلی" className="flex flex-wrap items-center justify-end gap-x-5 gap-y-2 text-sm font-bold text-ink/70">
          {links.map(([href, label]) => <Link key={href} href={href} className="transition hover:text-leaf">{label}</Link>)}
          <Link href="/consultation" className="rounded-full bg-forest px-5 py-2.5 text-white transition hover:bg-leaf">درخواست مشاوره</Link>
        </nav>
      </div>
    </header>
  );
}
