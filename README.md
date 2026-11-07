# Sabz Greenhouse

اسکلت MVP وب‌سایت شرکتی، خدمات تخصصی و کاتالوگ تجهیزات گلخانه‌ای. این مخزن در مرحله M0 است و هنوز شامل داده واقعی، مدل‌های دامنه یا APIهای تجاری نیست.

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
python backend\manage.py test apps.core.tests
Set-Location frontend
npm run lint
npm run build
```

هیچ secret واقعی نباید commit شود. فایل `.env` محلی است و از Git خارج شده است.
