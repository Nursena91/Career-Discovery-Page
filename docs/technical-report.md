# Teknik Rapor: Career Discovery Agent

## 1. Proje Tanımı

Bu proje, kariyer sitelerinden staj ve part-time ilanlarını toplayan, normalize eden, filtreleyen ve kullanıcıya uygun ilanları sıralayan bir ajan / ürün prototipidir. Amaç, kullanıcıların iş arama sürecini otomatikleştirmek ve kariyer fırsatlarını daha hızlı erişilebilir hale getirmektir.

## 2. İş Problemi

Kariyer siteleri ve şirket kariyer sayfaları, adayların erişmesi gereken veriyi yaygın biçimde dağıtmaktadır. Bu veriler:

- aynı ilana birden çok kaynaktan ulaşılabilir
- farklı formatlarda gelir
- staj, part-time ve full-time ayrımını net tutmaz
- kullanıcı profiline göre filtreleme gerektirir

Bu durum iş arama sürecini verimsiz hale getirir. Ürün, bu veri akışını birleştirip kullanıcı için uygun ve net bir sonuç üretmelidir.

## 3. Hedefler

### 3.1 İş hedefleri

- Kayıtlı kariyer kaynaklarından staj/part-time ilanları toplamak
- Veri standartlaştırma yapmak
- Kullanıcı özel eşleştirme ve sıralama sunmak
- Sonraki aşamada web dashboard ve bildirim sistemi kurmak

### 3.2 Teknik hedefler

- Modüler kaynak adaptörü mimarisi
- Dedupe sistemi
- Match scoring sistemi
- Test edilebilir API ve veri katmanı
- Ölçeklenebilir ve izlenebilir servis yapısı

## 4. Kullanıcı Profilleri

### Öğrenci / Yeni mezun

- Staj ya da part-time iş arıyor
- Lokasyon ve maaş kriterleri var
- Özgeçmiş / beceri ve ilgi alanı önemli

### Mevcut çalışan

- Yarı zamanlı ya da yan iş arıyor
- Esnek çalışma biçimi istiyor
- Sezonluk işlerde uyum aranıyor

## 5. Ürün Vizyonu

Bir “agent” değil, bir “kariyer bulma platformu” yaklaşımı benimsenmelidir. Ürün, kullanıcıya tek ekranda uygun iş fırsatlarını sunmalı ve iş başvurusu için tüm süreci kolaylaştırmalıdır.

## 6. Kaynak Stratejisi

### 6.1 Öncelikli kaynaklar

- LinkedIn Jobs
- Indeed
- Glassdoor
- Greenhouse
- Lever
- Workable
- Wellfound
- Otta
- Jooble
- Remote.co / We Work Remotely / Remotive
- Firma kariyer sayfaları

### 6.2 Sınırlamalar ve yaklaşım

Bazı kaynaklar scraping için kısıtlı olabilir. Bu nedenle ürün şu stratejiyi izleyecek:

- API erişimi olan kaynaklar öncelikli olacak
- Legal ve erişilebilir public kaynaklar 2. aşamada entegre edilecek
- Site kullanım şartları ve robots.txt kontrolü yapılacak
- Rate limit, IP ve anti-bot mekanizmaları dikkate alınacak

## 7. Mimari Yaklaşım

### 7.1 Ana katmanlar

1. Source adapters
2. Scheduler / queue manager
3. Extraction layer
4. Normalization layer
5. Deduplication layer
6. Enrichment layer
7. Match engine
8. Storage layer
9. API layer
10. Notification layer

## 8. Teknik Mimari

### 8.1 Backend

- Python
- FastAPI

### 8.2 Scraping ve işleme

- Playwright
- BeautifulSoup
- Selectolax
- Python async yapılar

### 8.3 Veri saklama

- PostgreSQL
- Redis
- İsteğe bağlı Elasticsearch veya pgvector

### 8.4 Çalıştırma

- Docker
- Docker Compose
- Celery + Redis for background tasks

## 9. Veri Modeli

### 9.1 Job model

- id
- source
- source_url
- title
- company_name
- company_url
- location
- remote_type
- contract_type
- role_type
- seniority
- description
- skills
- salary_range
- posted_at
- scraped_at
- normalized_tags
- hash_key

### 9.2 User profile model

- user_id
- preferred_roles
- preferred_locations
- contract_types
- skills
- degree
- min_salary
- saved_jobs
- alert_preferences

## 10. Dedupe Stratejisi

Aynı iş ilanı farklı sitelerde bulunabilir. Bu nedenle standart bir dedupe mekanizması şarttır.

### Kullanılacak yöntemler

- URL bazlı dedupe
- Title + company + location + description hash
- Fuzzy matching for near-duplicate records

Bu sistem, aynı işi birden fazla kez göstermeden tek bir kayıt döndürür.

## 11. Match Scoring

İlan uygunluğu şu kriterlerle hesaplanır:

- rol eşleşmesi
- beceri eşleşmesi
- lokasyon eşleşmesi
- çalışma tipi eşleşmesi
- deneyim seviyesi uyumu
- maaş uygunluğu
- remote / hybrid / onsite tercihi

Örnek formül:

match_score = 0.30 * role_match + 0.25 * skill_match + 0.20 * location_match + 0.10 * work_type_match + 0.10 * seniority_fit + 0.05 * salary_fit

## 12. İlk MVP Özellikleri

1. Kaynak adapter yapısı
2. Staj/part-time filtreleme
3. Dedupe sistemleri
4. Match scoring
5. Web API
6. Dashboard için temel endpointler

## 13. Riskler

### 13.1 Erişim engelleri

Kaynak siteleri erişimi kısıtlayabilir. Çözüm: API tabanlı kaynaklar, rate limiting ve modüler source adapter yaklaşımı.

### 13.2 Veri kalitesi

Farklı sayfalarda çakışan formatlar sonucu bozuk veri oluşabilir. Çözüm: validation ve normalization katmanı.

### 13.3 Hukuki ve etik kısıtlar

Web scraping bazı kaynaklar için yasadışı ya da kullanım şartlarına aykırı olabilir. Çözüm: kaynağa göre izin kontrolü ve uygun yöntemler.

## 14. Geliştirme Planı

### Aşama 1: Proje iskeleti

- repo kurulumu
- ortam yapısı
- README ve teknik dokümanlar
- FastAPI base app

### Aşama 2: Source adapters

- LinkedIn / Indeed / Greenhouse / Lever örnekleri
- Adapter base class
- html parsing ve normalization

### Aşama 3: Dedupe ve matcher

- hash-based dedupe
- kullanıcı eşleşme algoritması
- uygunluk skorları

### Aşama 4: Dashboard ve alerts

- kullanıcı profili
- favoriler
- e-posta / bildirim sistemi

### Aşama 5: Ölçeklendirme

- multi-source yönetimi
- yeni kullanıcı segmentleri
- robust monitoring

## 15. Sonuç

Bu proje, tek bir scraper değil, kullanıcı için anlamlı kariyer fırsat bulma sistemi kurmayı hedefler. Teknik olarak modüler, veri odaklı ve ürün odaklı bir yaklaşım gerektirir. Başlangıçta doğru mimari ve veri standardizasyonu oluşturulursa, sonraki aşamada güçlü bir ürün haline gelmesi mümkündür.
