import http from 'k6/http';
import { check, sleep } from 'k6';
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";
import { textSummary } from "https://jslib.k6.io/k6-summary/0.0.1/index.js";

export const options = {
  vus: 10,              // usuarios concurrentes
  duration: '1m',       // duración de la prueba
  thresholds: {
    http_req_duration: ['p(95)<600'], // 95% < 600 ms
    http_req_failed: ['rate<0.1'],     // menos del 10% de fallos
  },
};

// Datos para generar usuarios variados
const nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Laura', 'Pedro', 'Sofia', 'Diego', 'Camila'];
const apellidos = ['García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Flores'];
const generos = ['M', 'F'];
const dominios = ['unal.edu.co', 'gmail.com', 'hotmail.com', 'outlook.com'];

// Función para generar fecha de nacimiento aleatoria
function randomBirthDate() {
  const year = 1990 + Math.floor(Math.random() * 15); // Entre 1990-2004
  const month = String(Math.floor(Math.random() * 12) + 1).padStart(2, '0');
  const day = String(Math.floor(Math.random() * 28) + 1).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// Función para seleccionar elemento aleatorio de un array
function randomElement(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

// Función para generar número de documento único
function generateDocument() {
  return `${Math.floor(10000000 + Math.random() * 90000000)}`;
}

export default function () {
  const url = 'http://localhost:8001/users_unal/';

  // Generar datos de usuario aleatorios
  const nombre = randomElement(nombres);
  const apellido = randomElement(apellidos);
  const genero = randomElement(generos);
  const dominio = randomElement(dominios);
  
  // Crear email único combinando VU, iteración y timestamp
  const timestamp = Date.now();
  const email = `${nombre.toLowerCase()}.${apellido.toLowerCase()}.${__VU}.${__ITER}.${timestamp}@${dominio}`;
  
  const payload = JSON.stringify({
    email_unal: email,
    document: generateDocument(),
    name: nombre,
    lastname: apellido,
    full_name: `${nombre} ${apellido}`,
    gender: genero,
    birth_date: randomBirthDate(),
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(url, payload, params);

  check(res, {
    'status is success (2xx)': (r) => r.status >= 200 && r.status < 300,
    'status is 201 Created': (r) => r.status === 201,
    'response time < 600ms': (r) => r.timings.duration < 600,
    'response has body': (r) => r.body.length > 0,
  });

  // Log para debug (opcional, comentar en pruebas largas)
  if (res.status !== 201) {
    console.log(`Error: VU=${__VU}, Status=${res.status}, Body=${res.body}`);
  }

  sleep(Math.random() * 2 + 0.5); // Sleep aleatorio entre 0.5 y 2.5 segundos
}

// Generar reportes en múltiples formatos
export function handleSummary(data) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
  
  return {
    'test-results/create-users-summary.html': htmlReport(data),
    'test-results/create-users-summary.json': JSON.stringify(data, null, 2),
    'test-results/create-users-summary.txt': textSummary(data, { indent: ' ', enableColors: false }),
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}