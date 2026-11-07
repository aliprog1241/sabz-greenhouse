# قرارداد API نسخه ۱

مسیر پایه در توسعه `http://localhost:8000/api/v1` است. مستندات تعاملی در `/api/docs/` و schema خام در `/api/schema/` ارائه می‌شوند.

## مسیرهای فقط خواندنی

- `GET /products/?search=&category=&page=`
- `GET /products/{slug}/`
- `GET /categories/`
- `GET /services/` و `GET /services/{slug}/`
- `GET /projects/` و `GET /projects/{slug}/`
- `GET /certificates/`
- `GET /articles/` و `GET /articles/{slug}/`

فقط محتوای فعال و منتشرشده در API عمومی دیده می‌شود. فهرست محصولات با ۱۲ رکورد در هر صفحه صفحه‌بندی می‌شود و `category` نامک دسته را می‌پذیرد.

## ثبت استعلام محصول

`POST /quotations/`

```json
{
  "product_id": 1,
  "full_name": "نام درخواست‌کننده",
  "phone": "09121234567",
  "province": "تهران",
  "city": "تهران",
  "quantity": "2.00",
  "description": "توضیح اختیاری",
  "privacy_accepted": true,
  "website": ""
}
```

هویت محصول و واحد از پایگاه داده resolve می‌شود و کلاینت اجازه ارسال snapshot ندارد. سقف پیش‌فرض ۱۰ درخواست در ساعت برای هر IP است.

## ثبت مشاوره

`POST /consultations/`

```json
{
  "full_name": "نام درخواست‌کننده",
  "phone": "09121234567",
  "province": "فارس",
  "city": "شیراز",
  "crop_type": "گوجه‌فرنگی",
  "greenhouse_area": "1200.00",
  "service_id": 1,
  "cultivation_method": "هیدروپونیک",
  "problem_description": "شرح مسئله",
  "website": ""
}
```

فیلد `website` honeypot است و باید خالی بماند. سقف پیش‌فرض مشاوره ۵ درخواست در ساعت برای هر IP است.

پاسخ موفق هر دو فرم با وضعیت HTTP 201:

```json
{
  "success": true,
  "tracking_code": "SG-0123456789",
  "status": "NEW"
}
```

کد پیگیری صرفاً رسید ثبت درخواست است و مجوز دسترسی عمومی به اطلاعات درخواست محسوب نمی‌شود.
