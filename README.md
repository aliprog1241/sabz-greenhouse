# Sabz Greenhouse

MVP فنی وب‌سایت، کاتالوگ و پنل مدیریت سبز گلخانه. داده‌های واقعی کسب‌وکار هنوز باید از مسیر پنل مدیریت تأیید و تکمیل شوند.

## معماری

- `backend`: Django و Django REST Framework با PostgreSQL
- `frontend`: Next.js App Router، TypeScript و Tailwind CSS
- `docs`: تصمیم‌های معماری و دستور راه‌اندازی

## راه‌اندازی در Windows PowerShell

```powershell
Copy-Item .env.example .env
docker compose up -d db
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python backend\manage.py migrate
python backend\manage.py runserver
```

در ترمینال دوم:

```powershell
Set-Location frontend
npm install
npm run dev
```

فرانت‌اند در `http://localhost:3000`، API در `http://localhost:8000` و health check در `http://localhost:8000/api/v1/health/` در دسترس است.

## کنترل کیفیت M0

```powershell
python backend\manage.py check
python backend\manage.py test apps.core apps.catalog apps.leads --settings=config.settings_test
Set-Location frontend
npm run lint
npm run build
```

هیچ secret واقعی نباید commit شود. فایل `.env` محلی است و از Git خارج شده است.

## وضعیت توسعه

- M0: زیرساخت مونوریپو و محیط اجرا تکمیل شده است.
- M1: مدل‌های دامنه، migrationها و Django Admin تکمیل شده‌اند.
- M2: APIهای خواندنی، فرم‌های ثبت درخواست، rate limit، ضداسپم و OpenAPI تکمیل شده‌اند.
- M3: رابط عمومی فارسی RTL، صفحات P0، کاتالوگ و فرم‌های متصل به API تکمیل شده‌اند.
- M4: پنل مدیریت با عملیات انتشار گروهی، گردش وضعیت سرنخ‌ها، حفاظت از داده‌های ثبت‌شده و تنظیمات تک‌نمونه‌ای سخت‌سازی شده است.
- M5: استقرار Docker، reverse proxy، نگهداری پایدار رسانه و فرایند backup/restore آماده شده است.
- مرحله بعد: تأمین دامنه و TLS، staging و پایش عملیاتی در M6.

راهنمای استقرار تولید در `docs/deployment.md` قرار دارد.

قرارداد کامل endpointها در `docs/api.md` و Swagger در `http://localhost:8000/api/docs/` قرار دارد.
