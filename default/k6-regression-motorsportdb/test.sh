#!/bin/bash

set -e

# Chemin temporaire du script à tester
TMP_SCRIPT=/tmp/k6-script.js

# Écrire le contenu du script JS de test dans un fichier temporaire
cat <<'EOF' > "$TMP_SCRIPT"
import http from 'k6/http';
import { check } from 'k6';

export let options = {
    stages: [
        { duration: '15s', target: 20 },  // Up
        { duration: '45s', target: 1000 }, // Max Load
        { duration: '15s', target: 0 },   // Down
    ],
    thresholds: {
        http_req_duration: ['p(95)<1000'], // 95% of requests < 1s
        http_req_failed: ['rate<0.01'],    // Less than 1% failures
    },
};

const BASE_URL = 'http://localhost:80';

export default function () {
    const pages = [
        '/index.html',
        '/driver.html?id=Doriane_Pin',
        '/race.html?id=Formula_1&year=2025',
        '/team.html?id=Alpine_Renault',
    ];

    for (const path of pages) {
        let res = http.get(`${BASE_URL}${path}`);
        check(res, {
            [`${path} - status 200`]: (r) => r.status === 200,
        });
    }
}
EOF

echo "🔄 Copie du script dans le conteneur deploy-motorsportdb..."
docker cp "$TMP_SCRIPT" deploy-motorsportdb:/tmp/k6-script.js

echo "🚀 Lancement du test de charge avec k6..."
if docker exec deploy-motorsportdb k6 run /tmp/k6-script.js; then
  echo "✅ Test de charge réussi"
  exit 0
else
  echo "❌ Test de charge échoué"
  exit 1
fi
