# استقرار و پشتیبان‌گیری M5

استقرار مرجع MVP یک میزبان Linux دارای Docker Compose است. Caddy تنها درگاه عمومی است؛ فرانت‌اند، Django و PostgreSQL مستقیماً روی اینترنت منتشر نمی‌شوند. Caddy پس از تنظیم DNS، گواهی HTTPS را خودکار صادر و تمدید می‌کند.

## آماده‌سازی

1. فایل `.env.production.example` را با نام `.env.production` کپی کنید.
2. secretها، دامنه و رمز پایگاه داده را با مقادیر واقعی جایگزین کنید.
3. رکوردهای `A` و در صورت استفاده `AAAA` دامنه را به IP سرور اشاره دهید و پورت‌های 80 و 443 را باز کنید.
4. `SITE_DOMAIN` و `ACME_EMAIL` را مقداردهی کنید. گزینه‌های secure cookie و redirect در نمونه production فعال هستند و HSTS ابتدا با مقدار کم تنظیم شده است.
5. اجرا:

```powershell
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build
docker compose --env-file .env.production -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

بررسی سلامت:

```powershell
docker compose --env-file .env.production -f docker-compose.prod.yml ps
.\scripts\health-check.ps1 -BaseUrl https://example.com
```

## داده‌های پایدار

- `postgres_data`: پایگاه داده PostgreSQL
- `media_data`: تصاویر محصولات، پروژه‌ها و گواهی‌ها

این volumeها با حذف یا بازسازی container از بین نمی‌روند، ولی جایگزین بکاپ خارج از میزبان نیستند.

## پشتیبان‌گیری

```powershell
.\scripts\backup.ps1
```

خروجی زمان‌دار شامل `database.dump` و `media.tar.gz` است. پوشه `backups/` از Git خارج است و باید به فضای ذخیره‌سازی جداگانه منتقل شود.

بازیابی، داده فعلی پایگاه داده و رسانه را جایگزین می‌کند و باید فقط در پنجره نگهداری اجرا شود:

```powershell
.\scripts\restore.ps1 -BackupDirectory .\backups\YYYYMMDD-HHMMSS
```

پیش از اولین استقرار واقعی، یک چرخه کامل backup/restore در محیط staging آزمایش شود.

## محیط staging

فایل `.env.staging.example` را روی یک میزبان جدا به `.env.staging` تبدیل و دامنه staging را جایگزین کنید. نام پروژه Compose جداست تا volumeهای staging با production تداخل نکنند. اجرای هم‌زمان staging و production روی یک میزبان به طراحی شبکه و proxy مشترک نیاز دارد و در این الگو انجام نمی‌شود:

```powershell
$env:ENV_FILE = ".env.staging"
docker compose --env-file .env.staging -f docker-compose.prod.yml up -d --build
```

## CI و پایش

Workflow فایل `.github/workflows/ci.yml` در هر push و pull request تست‌های Django، lint/build فرانت‌اند، اعتبارسنجی Compose و ساخت هر دو image را اجرا می‌کند.

برای فعال‌کردن پایش ۱۵ دقیقه‌ای staging، در GitHub Actions secret زیر را ثبت کنید:

- `STAGING_HEALTH_URL`: آدرس کامل health check، مانند `https://staging.example.com/api/v1/health/`

تا پیش از ثبت secret، مانیتور بدون خطا skip می‌شود.
