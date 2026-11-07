export default function Home() {
  return (
    <main className="min-h-screen bg-[var(--background)] px-6 py-20 text-[var(--foreground)]">
      <section className="mx-auto max-w-6xl overflow-hidden rounded-[2rem] bg-[var(--brand-dark)] px-7 py-16 text-white shadow-2xl sm:px-12 lg:px-20">
        <p className="mb-6 text-sm font-semibold tracking-[0.18em] text-[var(--brand-gold)]">SABZ GREENHOUSE</p>
        <h1 className="max-w-3xl text-4xl font-bold leading-[1.45] sm:text-6xl">راهکارهای تخصصی برای گلخانه‌های حرفه‌ای</h1>
        <p className="mt-8 max-w-2xl text-lg leading-9 text-white/75">زیرساخت اولیه پلتفرم خدمات، پروژه‌ها و کاتالوگ تجهیزات گلخانه‌ای آماده شده است. محتوای واقعی پس از تأیید مجموعه جایگزین می‌شود.</p>
        <div className="mt-10 flex flex-wrap gap-4">
          <span className="rounded-full bg-[var(--brand-gold)] px-6 py-3 font-bold text-[var(--brand-dark)]">مرحله M0 تکمیل زیرساخت</span>
          <span className="rounded-full border border-white/25 px-6 py-3 text-white/80">بدون فروش آنلاین و پرداخت</span>
        </div>
      </section>
    </main>
  );
}
