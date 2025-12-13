import http from 'k6/http';
import { check, sleep } from 'k6';
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";
import { textSummary } from "https://jslib.k6.io/k6-summary/0.0.1/index.js";

export const options = {
  vus: 15,              // usuarios concurrentes (más alto para GET)
  duration: '1m',       // duración de la prueba
  thresholds: {
    http_req_duration: ['p(95)<400'], // 95% < 400 ms (más estricto para GET)
    http_req_failed: ['rate<0.05'],    // menos del 5% de fallos
    http_reqs: ['rate>50'],            // al menos 50 requests por segundo
  },
};

export default function () {
  const baseUrl = 'http://localhost:8001/users_unal/';
  
  // Escenario 1: GET de la lista completa (70% del tiempo)
  if (Math.random() < 0.7) {
    const res = http.get(baseUrl);
    
    check(res, {
      'GET list - status is 200': (r) => r.status === 200,
      'GET list - response time < 400ms': (r) => r.timings.duration < 400,
      'GET list - has body': (r) => r.body.length > 0,
      'GET list - is JSON': (r) => r.headers['Content-Type']?.includes('application/json'),
      'GET list - has results': (r) => {
        try {
          const body = JSON.parse(r.body);
          return Array.isArray(body) || (body.results && Array.isArray(body.results));
        } catch {
          return false;
        }
      },
    });

    // Validaciones adicionales del contenido
    if (res.status === 200) {
      try {
        const data = JSON.parse(res.body);
        const users = Array.isArray(data) ? data : data.results || [];
        
        check(users, {
          'GET list - has users': (u) => u.length > 0,
        });
        
        if (users.length > 0) {
          const firstUser = users[0];
          check(firstUser, {
            'GET list - user has email': (u) => !!u.email_unal,
            'GET list - user has document': (u) => !!u.document,
            'GET list - user has name': (u) => !!u.name,
          });
        }
      } catch (e) {
        console.log(`Error parsing JSON: ${e.message}`);
      }
    }
  }
  // Escenario 2: GET con paginación (20% del tiempo)
  else if (Math.random() < 0.85) {
    const page = Math.floor(Math.random() * 10) + 1; // Páginas 1-10
    const pageSize = [10, 20, 50][Math.floor(Math.random() * 3)]; // Tamaños variados
    
    const url = `${baseUrl}?page=${page}&page_size=${pageSize}`;
    const res = http.get(url);
    
    check(res, {
      'GET pagination - status is 200': (r) => r.status === 200,
      'GET pagination - response time < 400ms': (r) => r.timings.duration < 400,
      'GET pagination - has body': (r) => r.body.length > 0,
    });
    
    if (res.status === 200) {
      try {
        const data = JSON.parse(res.body);
        check(data, {
          'GET pagination - has pagination info': (d) => 
            (d.count !== undefined || d.results !== undefined) || Array.isArray(d),
        });
      } catch (e) {
        console.log(`Error parsing pagination: ${e.message}`);
      }
    }
  }
  // Escenario 3: GET con filtros/búsqueda (10% del tiempo)
  else {
    const searchTerms = ['test', 'user', 'gmail', 'unal'];
    const searchTerm = searchTerms[Math.floor(Math.random() * searchTerms.length)];
    
    const url = `${baseUrl}?search=${searchTerm}`;
    const res = http.get(url);
    
    check(res, {
      'GET search - status is 200': (r) => r.status === 200,
      'GET search - response time < 400ms': (r) => r.timings.duration < 400,
      'GET search - has body': (r) => r.body.length > 0,
    });
  }

  // Sleep aleatorio para simular comportamiento real
  sleep(Math.random() * 1.5 + 0.3); // Entre 0.3 y 1.8 segundos
}

// Setup: Función que se ejecuta una vez antes de la prueba
export function setup() {
  console.log('Iniciando prueba de GET /users_unal/');
  console.log('Verificando que el endpoint esté disponible...');
  
  const res = http.get('http://localhost:8001/users_unal/');
  if (res.status !== 200) {
    console.error(`Advertencia: El endpoint no responde correctamente (Status: ${res.status})`);
  } else {
    console.log('Endpoint disponible ✓');
  }
}

// Teardown: Función que se ejecuta una vez después de la prueba
export function teardown(data) {
  console.log('Prueba finalizada');
}

// Generar reportes en múltiples formatos
export function handleSummary(data) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
  
  return {
    'test-results/get-users-summary.html': htmlReport(data),
    'test-results/get-users-summary.json': JSON.stringify(data, null, 2),
    'test-results/get-users-summary.txt': textSummary(data, { indent: ' ', enableColors: false }),
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}