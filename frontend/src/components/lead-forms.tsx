"use client";

import { FormEvent, useState } from "react";
import { API_BASE } from "@/lib/api";
import type { Service, SubmissionResponse } from "@/types/api";

type FormState = { loading: boolean; success?: SubmissionResponse; error?: string };

async function submit(path: string, payload: Record<string, unknown>) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(Object.values(data).flat().join(" ") || "ثبت درخواست انجام نشد.");
  return data as SubmissionResponse;
}

function Result({ state }: { state: FormState }) {
  if (state.success) return <div role="status" className="rounded-2xl bg-leaf/10 p-5 text-forest"><strong>درخواست ثبت شد.</strong><p className="mt-2">کد پیگیری: <b dir="ltr">{state.success.tracking_code}</b></p></div>;
  if (state.error) return <div role="alert" className="rounded-2xl bg-red-50 p-5 text-red-800">{state.error}</div>;
  return null;
}

export function QuoteForm({ productId, productName, unit }: { productId: number; productName: string; unit: string }) {
  const [state, setState] = useState<FormState>({ loading: false });
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setState({ loading: true });
    const form = new FormData(event.currentTarget);
    try {
      const success = await submit("/quotations/", {
        product_id: productId, full_name: form.get("full_name"), phone: form.get("phone"),
        province: form.get("province"), city: form.get("city"), quantity: form.get("quantity"),
        description: form.get("description"), privacy_accepted: form.get("privacy_accepted") === "on",
        website: form.get("website"),
      });
      setState({ loading: false, success }); event.currentTarget.reset();
    } catch (error) { setState({ loading: false, error: error instanceof Error ? error.message : "خطای ناشناخته" }); }
  }
  return <form onSubmit={onSubmit} className="form-card">
    <div><p className="eyebrow">استعلام محصول</p><h2 className="mt-3 text-2xl font-black text-forest">{productName}</h2><p className="mt-2 text-sm text-ink/55">واحد ثبت‌شده: {unit}</p></div>
    <div className="form-grid"><label>نام و نام خانوادگی<input name="full_name" required /></label><label>شماره موبایل<input name="phone" dir="ltr" inputMode="tel" pattern="(?:\+98|0098|98|0)?9\d{9}" required /></label><label>استان<input name="province" required /></label><label>شهر<input name="city" /></label><label>تعداد<input name="quantity" dir="ltr" type="number" min="0.01" step="0.01" required /></label></div>
    <label>توضیحات<textarea name="description" rows={4} /></label><label className="hidden" aria-hidden>وب‌سایت<input name="website" tabIndex={-1} autoComplete="off" /></label>
    <label className="check"><input name="privacy_accepted" type="checkbox" required /> سیاست حریم خصوصی را مطالعه کرده‌ام و با ثبت اطلاعات موافقم.</label>
    <Result state={state} /><button className="button-primary" disabled={state.loading}>{state.loading ? "در حال ثبت…" : "ثبت درخواست استعلام"}</button>
  </form>;
}

export function ConsultationForm({ services, defaultServiceId }: { services: Service[]; defaultServiceId?: string }) {
  const [state, setState] = useState<FormState>({ loading: false });
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setState({ loading: true }); const form = new FormData(event.currentTarget);
    const service = form.get("service_id");
    try {
      const success = await submit("/consultations/", {
        full_name: form.get("full_name"), phone: form.get("phone"), province: form.get("province"), city: form.get("city"),
        crop_type: form.get("crop_type"), greenhouse_area: form.get("greenhouse_area"),
        cultivation_method: form.get("cultivation_method"), problem_description: form.get("problem_description"),
        ...(service ? { service_id: Number(service) } : {}), website: form.get("website"),
      });
      setState({ loading: false, success }); event.currentTarget.reset();
    } catch (error) { setState({ loading: false, error: error instanceof Error ? error.message : "خطای ناشناخته" }); }
  }
  return <form onSubmit={onSubmit} className="form-card">
    <div className="form-grid"><label>نام و نام خانوادگی<input name="full_name" required /></label><label>شماره موبایل<input name="phone" dir="ltr" inputMode="tel" required /></label><label>استان<input name="province" required /></label><label>شهر<input name="city" /></label><label>نوع کشت<input name="crop_type" required /></label><label>مساحت گلخانه متر مربع<input name="greenhouse_area" type="number" min="0.01" step="0.01" required /></label><label>روش کشت<input name="cultivation_method" /></label><label>خدمت مورد نظر<select name="service_id" defaultValue={defaultServiceId||""}><option value="">انتخاب نشده</option>{services.map(s => <option key={s.id} value={s.id}>{s.title}</option>)}</select></label></div>
    <label>شرح مسئله<textarea name="problem_description" rows={6} required /></label><label className="hidden" aria-hidden>وب‌سایت<input name="website" tabIndex={-1} autoComplete="off" /></label>
    <Result state={state} /><button className="button-primary" disabled={state.loading}>{state.loading ? "در حال ثبت…" : "ثبت درخواست مشاوره"}</button>
  </form>;
}
