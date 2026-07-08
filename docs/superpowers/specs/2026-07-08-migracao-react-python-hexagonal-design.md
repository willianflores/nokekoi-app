# Migração Nokekoi App: Streamlit → React (mobile-first) + Python (hexagonal)

## Contexto

O Nokekoi App monitora focos de calor (NASA FIRMS) e alertas de desmatamento (RADD) na Terra
Indígena Campinas/Katukina (Acre). Hoje é um app Streamlit monolítico (`nokekoi-app/`), com:

- `1_🔥_Foco_de_Calor.py` e `pages/2_🪵_Alerta_de_Desmatamento.py`: mapas Folium + cards de
  métricas, lendo arquivos GeoParquet pré-gerados por período (15d/30d/60d/90d/180d/365d).
- `scripts/`: ingestão via cron (`loadFirmsData.py`, `loadRaddData.py`, `tif_function.py`),
  gestão de token NASA (`token_manager.py`, `auto_renew_token.py`), envio de alerta por e-mail
  (`sendAlerts.py`), backup (`backup.sh`) e renovação SSL (`renew_ssl.sh`).
- Responsividade mobile obtida via overrides de CSS sobre o Streamlit
  (`mobile_responsive_improvements.py`), já que o framework não foi desenhado para mobile-first.
- Deploy: VM própria da UFAC, com Nginx (presumido) + certbot para HTTPS.

**Achado de segurança relevante (fora do escopo desta migração, tratado à parte):**
`scripts/sendAlerts.py` contém uma senha de e-mail em texto plano, commitada no histórico do git.
Não será corrigido como parte deste plano — está registrado aqui apenas como contexto conhecido.

O público-alvo (comunidades indígenas) acessa majoritariamente via celular, muitas vezes com
conexão instável. A demanda é reescrever o sistema com frontend em React (mobile-first) e
backend em Python, usando arquitetura limpa/hexagonal, com foco em segurança de dados e de
deploy/servidor.

## Decisões

- **Repositórios**: `nokekoi-js-app/` é o monorepo novo, com `frontend/`, `backend/`, `infra/`.
  `nokekoi-app/` (Streamlit) é aposentado ao final da migração (Fase 7), mas sua lógica de
  negócio e scripts de ingestão são portados, não descartados.
- **Pipeline de dados**: migrado para dentro da arquitetura hexagonal do backend (casos de uso +
  adapters), substituindo os scripts soltos.
- **Escopo do MVP**: paridade completa — mapa de focos de calor, mapa de desmatamento, métricas e
  alertas por e-mail, mobile-first, entregues antes do corte para produção.
- **Deploy**: mesmo servidor UFAC (VM própria), via Docker Compose + Nginx, mantendo Let's
  Encrypt/certbot.
- **Autenticação**: painel admin protegido (poucos usuários), login próprio (sem SSO/LDAP da
  UFAC), sessão via cookie httpOnly.
- **PWA/offline**: fora de escopo nesta fase — web responsivo online.
- **Armazenamento**: migração de GeoParquet/TIFF em disco para PostgreSQL + PostGIS.
- **Frontend**: React + Vite + TypeScript + Tailwind CSS + react-leaflet.
- **Backend**: FastAPI + PostGIS, com tipos do frontend gerados a partir do schema OpenAPI.

## Arquitetura de alto nível

```
nokekoi-js-app/
├── frontend/    # React (mobile-first)
├── backend/     # Python (arquitetura hexagonal)
└── infra/       # docker-compose, nginx, scripts de deploy
```

Fluxo: React (SPA mobile-first) → API REST (FastAPI) → Casos de uso (domínio) → Repositórios
(PostGIS). Um worker (Celery beat/APScheduler) roda os jobs de ingestão (FIRMS, RADD, alertas por
e-mail) como casos de uso do domínio, não como scripts soltos.

## Backend: arquitetura hexagonal

```
backend/
├── domain/                 # Regras de negócio puras, sem dependências externas
│   ├── entities/            # FireHotspot, DeforestationAlert, TerritoryBoundary, AdminUser
│   ├── value_objects/       # TimeRange (15d/30d/.../1a), AreaHectares, Coordinates
│   └── services/            # Cálculo de área (ha), agregação de métricas
│
├── application/             # Casos de uso (orquestram domínio + portas)
│   ├── use_cases/
│   │   ├── get_fire_hotspots.py        # substitui getFireData()
│   │   ├── get_deforestation_alerts.py # substitui getRaddData()
│   │   ├── ingest_firms_data.py         # substitui loadFirmsData.py
│   │   ├── ingest_radd_data.py          # substitui loadRaddData.py
│   │   ├── send_alert_notification.py   # substitui sendAlerts.py (sem senha hardcoded)
│   │   └── authenticate_admin.py
│   └── ports/                # Interfaces (contratos) — nada de SQL/HTTP aqui
│       ├── fire_repository.py
│       ├── deforestation_repository.py
│       ├── territory_repository.py
│       ├── notification_sender.py
│       └── external_fire_data_source.py  # contrato p/ NASA FIRMS API
│
├── adapters/                 # Implementações concretas das portas
│   ├── inbound/http/          # Rotas FastAPI, DTOs de request/response
│   └── outbound/
│       ├── postgis/           # Implementação dos repositórios (PostGIS)
│       ├── nasa_firms_api/    # Cliente HTTP para NASA FIRMS
│       ├── radd_api/          # Cliente HTTP para RADD
│       └── smtp_email/        # Envio de e-mail (credenciais via env/secrets)
│
└── infrastructure/            # DI, scheduler, settings (Pydantic Settings)
```

Regra de dependência: `domain` não importa nada; `application` só importa `domain` e define
`ports`; `adapters` implementam `ports`; `infrastructure` conecta tudo via injeção de dependência
(`Depends(...)` do FastAPI). Cada caso de uso é testável isoladamente com fakes das portas, sem
precisar do FastAPI nem do banco rodando.

## Modelo de dados (PostgreSQL + PostGIS)

```sql
territories (id, name, geom POLYGON, kind)              -- TI / buffer 10km
fire_hotspots (id, territory_id FK, geom POINT, acq_date, confidence, source)
deforestation_alerts (id, territory_id FK, geom POLYGON, alert_date, area_ha, source)
admin_users (id, email, password_hash, created_at, last_login)
alert_recipients (id, email, active)
ingestion_runs (id, source, started_at, finished_at, status, records_ingested)
```

- Índices `GIST` em `geom` + índice em `acq_date`/`alert_date`: filtro "últimos N dias na TI" via
  query, não via arquivo pré-computado por período.
- `area_ha` calculado via `ST_Area(ST_Transform(geom, <proj_area_equal>))`, mesma projeção
  `+proj=aea...` usada hoje, como função SQL/repositório.
- `ingestion_runs` dá visibilidade (painel admin) de execução e falhas do pipeline — hoje as
  falhas dos scripts cron são silenciosas.
- TIFFs do RADD continuam processados por rasterio no adapter de ingestão; o resultado (polígonos
  + área) vai para o Postgres, não para arquivo.

## Frontend (React mobile-first)

```
frontend/
├── src/
│   ├── domain/            # Tipos TS gerados do OpenAPI (FireHotspot, DeforestationAlert...)
│   ├── application/       # Hooks de caso de uso (useFireHotspots, useDeforestationAlerts)
│   ├── infrastructure/    # Cliente HTTP, config de API base URL
│   ├── ui/
│   │   ├── pages/          # HomePage, DeforestationPage, AdminPage
│   │   ├── components/     # MapView, MetricCard, TimeRangeSelector, MobileHeader
│   │   └── layout/         # AppShell (bottom nav mobile / sidebar desktop)
│   └── App.tsx
```

- Bottom navigation em telas < 768px (não sidebar) — resolve nativamente o que hoje é gambiarra
  de CSS sobre o Streamlit.
- `react-leaflet` com as mesmas camadas atuais (TI, buffer, focos de calor, alertas, legendas,
  fullscreen, geolocalização do usuário).
- Cards de métrica como componentes Tailwind reutilizáveis (grid 1 coluna mobile, 2 colunas
  desktop), portando o layout visual atual sem os blocos de HTML embutido via `st.markdown`.
- TypeScript com tipos gerados do schema OpenAPI do backend (`openapi-typescript`), mantendo
  frontend e backend sincronizados sem trabalho manual.
- Sem PWA/offline nesta fase.
- Admin (login + gestão de destinatários + status de ingestão) em rota protegida, consumindo os
  mesmos endpoints REST com cookie de sessão.

## Autenticação/admin

- Sessão via cookie `httpOnly` + `Secure` + `SameSite=Strict` (não JWT em localStorage).
- Sessão armazenada no Postgres ou Redis, expiração curta (~8h) com renovação.
- Senha com **argon2id**.
- Rate limiting no login (ex: 5 tentativas/15min por IP).
- CSRF: `SameSite=Strict` + verificação de header custom nas rotas de mutação do admin.
- Sem cadastro público: admins criados via CLI (`create-admin`), não há rota pública de signup.

## Segurança da aplicação e dados

- Segredos via variáveis de ambiente/Docker secrets (permissão `600`), nunca versionados nem
  hardcoded.
- HTTPS obrigatório; backend e Postgres não expostos publicamente (bind em rede interna Docker).
- Headers de segurança no Nginx: HSTS, `X-Content-Type-Options`, `X-Frame-Options`, CSP restritiva
  (superfície menor que hoje, já que o Folium injeta JS de CDNs externos).
- Validação de entrada via Pydantic em todas as rotas.
- `pip-audit`/`npm audit` no CI, Dependabot ativado.
- Backup automatizado do Postgres com retenção, idealmente com cópia fora do servidor.
- Logs de auditoria: login de admin, reprocessamento manual, alterações de destinatários de
  alerta.

## Deploy/infra no servidor UFAC

```
[Internet] → Nginx (80/443, Let's Encrypt/certbot)
                │
                ├── / (443)    → frontend (build estático)
                └── /api (443) → backend FastAPI (proxy_pass)

Docker Compose (rede interna, só Nginx exposto ao host):
  - nginx | frontend | backend | worker (Celery/APScheduler) | postgres (PostGIS) | redis
```

- Containers rodando como usuário não-root; Postgres com usuário de app sem privilégio de
  superuser.
- Firewall (ufw): só 22 (SSH por chave + fail2ban), 80, 443.
- SSH hardening: sem login root, só chave.
- `unattended-upgrades` para patches de segurança do SO.
- Certbot via cron/systemd timer, renovando o certificado usado pelo Nginx do Compose.
- Healthcheck do Compose + endpoint `/health`; alerta por e-mail se o worker de ingestão falhar N
  vezes seguidas.
- CI/CD: GitHub Actions builda imagens, roda testes + auditoria de dependências, deploy via SSH a
  partir da branch `main` protegida.

## Roadmap de fases

1. **Fase 0 — Fundação**: scaffold do monorepo, Docker Compose local (Postgres/PostGIS), esqueleto
   das camadas hexagonais com testes de exemplo, CI básico.
2. **Fase 1 — Dados**: schema PostGIS (Alembic), casos de uso de ingestão portando
   `loadFirmsData.py`/`loadRaddData.py`/`tif_function.py`, backfill único dos GeoParquet/TIFF
   existentes para o banco.
3. **Fase 2 — API**: endpoints REST (`/fire-hotspots`, `/deforestation-alerts`, `/territories`,
   `/metrics`) + autenticação admin (login, sessão, seed do primeiro admin).
4. **Fase 3 — Frontend core**: shell mobile-first, páginas de mapa, cards de métrica, consumindo a
   API.
5. **Fase 4 — Admin**: login, gestão de destinatários de alerta, painel de status de ingestão.
6. **Fase 5 — Alertas**: worker agendado reescrevendo `sendAlerts.py` como caso de uso, sem
   credencial hardcoded, com thresholds configuráveis.
7. **Fase 6 — Hardening & deploy**: Nginx + headers de segurança + firewall + backups + CI/CD
   publicando no servidor UFAC.
8. **Fase 7 — Corte**: paralelo por período de validação, depois desativar o Streamlit
   (`nokekoi-app`) e apontar DNS para a nova stack.

## Fora de escopo

- Correção da senha hardcoded em `sendAlerts.py` (achado registrado, tratado separadamente).
- PWA/cache offline.
- Integração com SSO/LDAP da UFAC.
- Cadastro público de usuários admin.
