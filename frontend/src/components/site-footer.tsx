import Link from "next/link";

export function SiteFooter() {
  return (
    <footer className="mt-24 bg-navy text-white">
      <div className="shell grid gap-10 py-14 md:grid-cols-3">
        <div><p className="text-xl font-black">Sabz Greenhouse</p><p className="mt-4 max-w-sm leading-8 text-white/65">بستر معرفی خدمات تخصصی و تجهیزات گلخانه‌ای؛ اطلاعات رسمی تماس و مجوزها پس از تأیید مجموعه درج می‌شوند.</p></div>
        <div><p className="font-bold text-gold">دسترسی سریع</p><div className="mt-4 flex flex-col gap-3 text-white/70"><Link href="/products">کاتالوگ محصولات</Link><Link href="/services">خدمات تخصصی</Link><Link href="/projects">پروژه‌ها</Link></div></div>
        <div><p className="font-bold text-gold">اطلاعات</p><div className="mt-4 flex flex-col gap-3 text-white/70"><Link href="/contact">تماس با ما</Link><Link href="/privacy">حریم خصوصی</Link><Link href="/consultation">فرم مشاوره</Link></div></div>
      </div>
      <div className="border-t border-white/10 py-5 text-center text-sm text-white/45">نام تجاری موقت — محتوای تأییدنشده با داده واقعی جایگزین خواهد شد.</div>
    </footer>
  );
}
