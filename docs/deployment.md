# استقرار و پشتیبان‌گیری M5

استقرار مرجع MVP یک میزبان Linux دارای Docker Compose است. Nginx تنها درگاه عمومی است؛ فرانت‌اند، Django و PostgreSQL مستقیماً روی اینترنت منتشر نمی‌شوند.

## آماده‌سازی

1. فایل `.env.production.example` را با نام `.env.production` کپی کنید.
2. secretها، دامنه و رمز پایگاه داده را با مقادیر واقعی جایگزین کنید.
3. تا پیش از فعال‌کردن HTTPS در لایه میزبان، گزینه‌های secure cookie و redirect را `false` نگه دارید. پس از TLS آن‌ها را `true` و HSTS را ابتدا با مقدار کم فعال کنید.
4. اجرا:

```powershell
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build
docker compose --env-file .env.production -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

بررسی سلامت:

```powershell
docker compose --env-file .env.production -f docker-compose.prod.yml ps
Invoke-WebRequest http://localhost/api/v1/health/
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
