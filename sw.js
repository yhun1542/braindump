/**
 * Synapse Brain — Service Worker
 * jasoneye.com PWA
 *
 * 전략:
 *   - HTML(navigate): 네트워크 우선 → 실패 시 캐시 (항상 최신 앱 제공)
 *   - 정적 리소스(아이콘/폰트): 캐시 우선 → 없으면 네트워크
 *   - Firebase/외부 CDN: SW 관여 없음 (크로스오리진)
 *
 * 업데이트:
 *   - CACHE 버전 올리면 구버전 캐시 자동 삭제
 *   - 업데이트 토스트에서 SKIP_WAITING 메시지로 즉시 반영
 */

const CACHE_VERSION = 'pwa-v51';
const SHELL_ASSETS = [
  '/',
  '/index.html',
  '/galaxy.html',
  '/iphone.html',
  '/firebase-bundle.js',
  '/manifest.webmanifest',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/icons/apple-touch-icon.png',
  '/favicon.ico',
  '/images/og-image.png',
  '/fonts/GmarketSansMedium.otf',
  '/fonts/GmarketSansBold.otf',
  '/fonts/GmarketSansLight.otf',
  '/fonts/GmarketSansTTFBold.ttf',
  '/fonts/GmarketSansTTFLight.ttf'
];

// ── Install: 셸 에셋 사전 캐시 ──────────────────────────────────────────────
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => {
      // 개별 실패가 전체를 막지 않도록 Promise.allSettled 사용
      return Promise.allSettled(
        SHELL_ASSETS.map((url) =>
          cache.add(url).catch((err) => {
            console.warn('[SW] 캐시 실패:', url, err.message);
          })
        )
      );
    }).then(() => {
      // 캐싱 완료 후 즉시 활성화 (waiting 상태 없이)
      return self.skipWaiting();
    })
  );
});

// ── Activate: 구버전 캐시 정리 ──────────────────────────────────────────────
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) =>
      Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_VERSION)
          .map((name) => {
            console.log('[SW] 구버전 캐시 삭제:', name);
            return caches.delete(name);
          })
      )
    ).then(() => self.clients.claim())
  );
});

// ── Fetch: 요청 처리 전략 ────────────────────────────────────────────────────
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // 크로스오리진 요청(Firebase, Google API, CDN 등)은 SW 관여 없음
  if (url.origin !== self.location.origin) return;

  // GET 요청만 캐시 처리
  if (req.method !== 'GET') return;

  const isNavigate = req.mode === 'navigate' ||
    (req.headers.get('accept') || '').includes('text/html');

  if (isNavigate) {
    // HTML: 네트워크 우선 → 실패 시 캐시 (항상 최신 버전 제공)
    event.respondWith(
      fetch(req, { cache: 'no-store' })
        .then((res) => {
          if (res.ok) {
            const copy = res.clone();
            caches.open(CACHE_VERSION).then((c) => {
              // 루트 경로는 index.html로 저장
              const cacheKey = url.pathname === '/' ? '/index.html' : req;
              c.put(cacheKey, copy);
            });
          }
          return res;
        })
        .catch(() => {
          // 오프라인: 캐시된 HTML 반환
          return caches.match(req)
            .then((cached) => cached || caches.match('/index.html'))
            .then((fallback) => {
              if (fallback) return fallback;
              // 완전 오프라인 폴백 응답
              return new Response(
                `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#0B1220">
  <title>Synapse Brain — 오프라인</title>
  <style>
    body { background:#0B1220; color:#e2e8f0; font-family:system-ui,-apple-system,sans-serif;
           display:flex; align-items:center; justify-content:center; min-height:100vh; margin:0; }
    .wrap { text-align:center; padding:2rem; }
    .icon { font-size:3rem; margin-bottom:1rem; }
    h1 { font-size:1.25rem; margin:0 0 .5rem; }
    p  { font-size:.875rem; opacity:.6; margin:0 0 1.5rem; }
    button { background:#6C63FF; color:#fff; border:0; padding:.75rem 1.5rem;
             border-radius:.75rem; font-size:.875rem; font-weight:600; cursor:pointer; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="icon">📡</div>
    <h1>인터넷 연결이 필요해요</h1>
    <p>Synapse Brain은 Firebase와 연결되어 있어<br>오프라인에서는 일부 기능이 제한됩니다.</p>
    <button onclick="location.reload()">다시 시도</button>
  </div>
</body>
</html>`,
                {
                  status: 200,
                  headers: {
                    'Content-Type': 'text/html; charset=utf-8',
                    'Cache-Control': 'no-store'
                  }
                }
              );
            });
        })
    );
    return;
  }

  // 정적 리소스(아이콘, 폰트 등): 캐시 우선 → 없으면 네트워크 후 캐시 저장
  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req).then((res) => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE_VERSION).then((c) => c.put(req, copy));
        }
        return res;
      }).catch(() => {
        // 정적 리소스 오프라인 실패는 조용히 처리
        return new Response('', { status: 503 });
      });
    })
  );
});

// ── Message: 업데이트 토스트에서 SKIP_WAITING 수신 ─────────────────────────
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    console.log('[SW] SKIP_WAITING 수신 — 즉시 활성화');
    self.skipWaiting();
  }
});
