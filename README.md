# Career Discovery Agent

Bir kariyer arama ajanı ve ürün fikri. Bu proje, stajyerlik ve part-time pozisyonları farklı kariyer sitelerinden toplayarak, normalize ederek, filtreleyerek ve kullanıcıya uygun ilanları sıralayan bir sistem kurmayı hedefler.

## Amaç

- Bilinen kariyer sitelerinden ilan toplamak
- Staj / part-time / internship / seasonal pozisyonları ayırmak
- Aynı ilanı birden fazla kaynaktan tek kez tutmak
- Kullanıcı profilini ve tercihlerini işin içine katmak
- Sonrasında web arayüzü ve bildirimler içeren bir ürün haline gelmek

## Hedef kullanıcı

- Öğrenciler
- Yeni mezunlar
- Part-time arayan profesyoneller
- Staj fırsatı arayan adaylar

## Ürün vizyonu

Bu işin tek amacı bir script yazmak değil; kullanıcıya zaman kazandıran, uygun iş fırsatlarını otomatik olarak sunan bir kariyer asistanı kurmaktır.

## Çözüm yaklaşımı

1. Kaynak yöneticisi ve scraper adaptörleri
2. Veri normalizasyon katmanı
3. Dedupe (aynı ilanı tek kez tutma)
4. Match scoring engine
5. API + dashboard + alerts

## Proje stack önerisi

- Backend: Python + FastAPI
- Scheduler: Celery + Redis
- Scraping: Playwright + BeautifulSoup
- Veritabanı: PostgreSQL
- Arama ve filtreleme: PostgreSQL / Elasticsearch (gelişmiş sürüm)
- Container: Docker
- Gösterim: Swagger / OpenAPI

## Repo yapısı

```text
career-discovery-agent/
├── README.md
├── .gitignore
├── docs/
│   ├── product-roadmap.md
│   └── technical-report.md
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       └── api/
│           ├── __init__.py
│           └── routes/
│               └── health.py
└── .github/
    └── workflows/
```

## İlk adım

Bu repo ilk iskelet olarak hazırlanmıştır. Bir sonraki adımda:

- kaynaklar için adapter katmanı
- veri şeması
- scraping service yapısı
- dedupe stratejisi
- ilk FastAPI endpointleri

oluşturulacak.

## Hızlı başlangıç

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Geliştirme notları

- Kaynak erişimi ve kalıcı veri toplanması için etki alanı bazlı modüler yapı kullanılacak.
- Her kaynak ayrı adapter ile yönetilecek.
- Dedupe, veri temizliği ve eşleştirme katmanı ana değer üreticidir.
- Bu iş sadece “scrape” değil, “kariyer eşleştirme ve karar desteği” olarak düşünülmelidir.

## Lisans

Tüm hakları proje sahibi tarafınca yönetilir. Bu repo eğitim, prototip ve ürün başlangıcı amacıyla oluşturulmuştur.
