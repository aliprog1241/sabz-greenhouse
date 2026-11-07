import Link from "next/link";
import { apiGet, resultsOf } from "@/lib/api";
import type { Category, Paginated, Product } from "@/types/api";
import { EmptyState, PageHero } from "@/components/ui";

export const dynamic="force-dynamic";
export const metadata={title:"محصولات"};
export default async function ProductsPage({searchParams}:{searchParams:Promise<{search?:string;category?:string;page?:string}>}){
  const q=await searchParams; const query=new URLSearchParams(); if(q.search)query.set("search",q.search);if(q.category)query.set("category",q.category);if(q.page)query.set("page",q.page);
  const [data,categories]=await Promise.all([apiGet<Paginated<Product>>(`/products/?${query}`),apiGet<Category[]>("/categories/")]); const products=resultsOf(data);
  const page=Math.max(1,Number(q.page)||1);const makePage=(n:number)=>{const p=new URLSearchParams();if(q.search)p.set("search",q.search);if(q.category)p.set("category",q.category);p.set("page",String(n));return`/products?${p}`};
  return <main><PageHero eyebrow="کاتالوگ" title="تجهیزات و نهاده‌های گلخانه‌ای" description="محصول مورد نظر را جستجو کنید و برای همان محصول یک درخواست استعلام مستقل ثبت کنید."/><section className="shell pb-20"><form className="card mb-8 grid gap-4 md:grid-cols-[1fr_240px_auto]"><input name="search" defaultValue={q.search} placeholder="جستجوی نام، برند یا کد محصول"/><select name="category" defaultValue={q.category||""}><option value="">همه دسته‌ها</option>{(categories||[]).map(c=><option key={c.id} value={c.slug}>{c.name}</option>)}</select><button className="button-primary">اعمال فیلتر</button></form>{products.length?<><div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">{products.map(p=><article className="card" key={p.id}><p className="text-sm font-bold text-leaf">{p.category.name}</p><h2 className="mt-3 text-xl font-black text-forest">{p.name}</h2><p className="mt-3 text-ink/55">{p.brand||"برند ثبت نشده"} · {p.unit}</p><Link className="button-secondary mt-7 w-full" href={`/products/${p.slug}`}>جزئیات و ثبت استعلام</Link></article>)}</div><nav aria-label="صفحه‌بندی محصولات" className="mt-8 flex justify-center gap-3">{data?.previous&&<Link className="button-secondary" href={makePage(page-1)}>صفحه قبل</Link>}{data?.next&&<Link className="button-primary" href={makePage(page+1)}>صفحه بعد</Link>}</nav></>:<EmptyState text="محصولی مطابق فیلترها پیدا نشد یا هنوز محصولی منتشر نشده است."/>}</section></main>;
}
