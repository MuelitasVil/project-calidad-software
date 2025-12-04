# Componentes Reutilizables - ORGSECURE Frontend

## 📋 Descripción

Este documento describe el sistema de componentes reutilizables implementado para mantener consistencia en el navbar y footer de todas las páginas del frontend de ORGSECURE.

## 🎯 Objetivo

Centralizar el código de navbar y footer para:
- ✅ Mantener consistencia visual en todas las páginas
- ✅ Facilitar mantenimiento y actualizaciones
- ✅ Reducir código duplicado
- ✅ Simplificar el desarrollo de nuevas páginas

## 📁 Estructura de Componentes

```
front/
├── components/
│   ├── navbar.js          # Componente de navegación
│   └── footer.js          # Componente de pie de página
├── index.html             # Página de inicio (usa footer)
├── login.html             # Página de login (usa footer)
├── dashboard.html         # Dashboard (usa navbar + footer)
└── compose-email.html     # Correo (usa navbar + footer)
```

## 🔧 Componentes Disponibles

### 1. Navbar Component (`components/navbar.js`)

Barra de navegación con logo, usuario y acciones de navegación.

#### Características:
- Logo y título ORGSECURE
- Display de usuario autenticado
- Botón de navegación contextual (Dashboard ↔ Correo)
- Botón de logout con confirmación
- Verificación automática de autenticación
- Iconos de Feather Icons

#### Uso básico:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Mi Página</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
  <script src="components/navbar.js"></script>
</head>
<body class="bg-gray-100 min-h-screen flex flex-col">
  
  <!-- Navbar Container -->
  <div id="navbar-container"></div>

  <!-- Tu contenido aquí -->
  <div class="flex-grow">
    <!-- ... -->
  </div>

  <script>
    // Verificar autenticación (redirige a login si no hay token)
    Navbar.checkAuth();

    // Renderizar navbar
    const navbar = new Navbar();
    navbar.render('navbar-container', { 
      currentPage: 'dashboard' // o 'compose-email'
    });
  </script>
</body>
</html>
```

#### Opciones de configuración:

```javascript
navbar.render('navbar-container', {
  currentPage: 'dashboard' // 'dashboard' | 'compose-email'
});
```

- **currentPage**: Define la página actual para mostrar el botón de navegación correcto
  - `'dashboard'`: Muestra botón "Correo" → navega a compose-email.html
  - `'compose-email'`: Muestra botón "Períodos" → navega a dashboard.html

#### Métodos estáticos:

```javascript
// Verificar autenticación (usar al inicio de cada página protegida)
Navbar.checkAuth(); // Retorna true si hay token, false y redirige a login si no
```

---

### 2. Footer Component (`components/footer.js`)

Pie de página con información institucional y enlaces.

#### Características:
- Logo y copyright automático (año actual)
- Enlaces de navegación opcionales
- Información institucional (Universidad Nacional de Colombia)
- Soporte para temas claro/oscuro
- Versión minimalista disponible

#### Uso básico:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Mi Página</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <script src="components/footer.js"></script>
</head>
<body class="bg-gray-100 min-h-screen flex flex-col">
  
  <!-- Tu contenido aquí -->
  <div class="flex-grow">
    <!-- ... -->
  </div>

  <!-- Footer Container -->
  <div id="footer-container"></div>

  <script>
    const footer = new Footer();
    
    // Footer completo con enlaces
    footer.render('footer-container', { 
      theme: 'light',      // 'light' | 'dark'
      showLinks: true      // true | false
    });

    // O footer minimalista (solo copyright)
    // footer.renderMinimal('footer-container');
  </script>
</body>
</html>
```

#### Opciones de configuración:

```javascript
// Footer completo
footer.render('footer-container', {
  theme: 'light',       // 'light' (blanco) | 'dark' (gris oscuro)
  showLinks: true       // true (muestra enlaces) | false (solo copyright)
});

// Footer minimalista
footer.renderMinimal('footer-container');
```

---

## 🚀 Implementación en Páginas

### Página con Navbar y Footer (Páginas Protegidas)

Ejemplo: `dashboard.html`, `compose-email.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ORGSECURE - Dashboard</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
  <script src="components/navbar.js"></script>
  <script src="components/footer.js"></script>
</head>
<body class="bg-gray-100 min-h-screen flex flex-col">
  
  <!-- Navbar Container -->
  <div id="navbar-container"></div>

  <!-- Contenido Principal -->
  <div class="flex-grow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Tu contenido aquí -->
    </div>
  </div>

  <!-- Footer Container -->
  <div id="footer-container"></div>

  <!-- Inicializar componentes -->
  <script>
    // Verificar autenticación
    Navbar.checkAuth();

    // Renderizar navbar
    const navbar = new Navbar();
    navbar.render('navbar-container', { currentPage: 'dashboard' });

    // Renderizar footer
    const footer = new Footer();
    footer.render('footer-container', { theme: 'light', showLinks: true });

    // Tu lógica de página aquí...
  </script>
</body>
</html>
```

### Página Solo con Footer (Páginas Públicas)

Ejemplo: `index.html`, `login.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ORGSECURE - Login</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <script src="components/footer.js"></script>
</head>
<body class="bg-gray-100 min-h-screen flex flex-col">
  
  <!-- Contenido Principal -->
  <div class="flex-grow">
    <!-- Tu contenido aquí -->
  </div>

  <!-- Footer Container -->
  <div id="footer-container"></div>

  <script>
    const footer = new Footer();
    footer.renderMinimal('footer-container');
  </script>
</body>
</html>
```

---

## 📐 Estructura HTML Recomendada

Para que los componentes funcionen correctamente con el layout, usa esta estructura:

```html
<body class="bg-gray-100 min-h-screen flex flex-col">
  
  <!-- Navbar (opcional) -->
  <div id="navbar-container"></div>

  <!-- Contenido principal (flex-grow para ocupar espacio disponible) -->
  <div class="flex-grow">
    <!-- Tu contenido aquí -->
  </div>

  <!-- Footer (siempre al final) -->
  <div id="footer-container"></div>

</body>
```

**Importante:** 
- El `body` debe tener `flex flex-col` para layout vertical
- El contenido principal debe tener `flex-grow` para ocupar espacio disponible
- Esto asegura que el footer siempre esté al final de la página

---

## 🎨 Personalización

### Cambiar colores del Navbar

Edita `components/navbar.js`:

```javascript
// Línea ~25
container.innerHTML = `
  <nav class="bg-white shadow-sm">  <!-- Cambia bg-white por otro color -->
```

### Cambiar información del Footer

Edita `components/footer.js`:

```javascript
// Línea ~50
<p>Universidad Nacional de Colombia</p>  <!-- Cambia el texto -->
```

### Agregar nuevos enlaces al Footer

Edita el método `renderLinks()` en `components/footer.js`:

```javascript
renderLinks(linkClass) {
  return `
    <div class="flex gap-4 text-sm">
      <a href="#" class="${linkClass}">Ayuda</a>
      <a href="#" class="${linkClass}">Mi Nuevo Enlace</a>  <!-- Agregar aquí -->
    </div>
  `;
}
```

---

## 🔒 Autenticación

El componente Navbar incluye verificación de autenticación:

```javascript
// Verifica si hay token en localStorage
Navbar.checkAuth(); // Redirige a login.html si no hay token
```

**Datos almacenados en localStorage:**
- `authToken`: JWT token de autenticación
- `user`: Objeto JSON con datos del usuario

**Ejemplo de usuario:**
```json
{
  "username": "john.doe",
  "email": "john@example.com",
  "role": "admin"
}
```

---

## 🔄 Flujo de Navegación

```
index.html (inicio)
    ↓
login.html (autenticación)
    ↓
dashboard.html ←→ compose-email.html
    ↓ (logout)
login.html
```

- **index.html** → **login.html**: Botón "Iniciar Sesión"
- **login.html** → **dashboard.html**: Login exitoso
- **dashboard.html** ↔ **compose-email.html**: Botones de navegación en navbar
- **Logout**: Cualquier página protegida → login.html

---

## 🐛 Troubleshooting

### El navbar no aparece

✅ **Verificar:**
1. Archivo `components/navbar.js` está cargado en el `<head>`
2. Existe un `<div id="navbar-container"></div>` en el HTML
3. Script de inicialización está al final del `<body>`
4. Feather Icons está cargado: `<script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>`

### Los iconos no se muestran

✅ **Verificar:**
1. Feather Icons está cargado
2. Se llama `feather.replace()` después de renderizar (ya incluido en navbar.js)

### El footer no está al final de la página

✅ **Verificar:**
1. El `<body>` tiene las clases: `flex flex-col min-h-screen`
2. El contenedor principal tiene la clase: `flex-grow`

### Error "Navbar is not defined"

✅ **Verificar:**
1. El archivo `components/navbar.js` está cargado ANTES del script de inicialización
2. La ruta es correcta: `<script src="components/navbar.js"></script>`

---

## 📝 Checklist para Nueva Página

Al crear una nueva página que use los componentes:

- [ ] Agregar Tailwind CSS en el `<head>`
- [ ] Agregar Feather Icons si usa navbar
- [ ] Agregar `<script src="components/navbar.js"></script>` (si usa navbar)
- [ ] Agregar `<script src="components/footer.js"></script>` (si usa footer)
- [ ] Agregar `class="flex flex-col min-h-screen"` al `<body>`
- [ ] Agregar `<div id="navbar-container"></div>` (si usa navbar)
- [ ] Agregar `class="flex-grow"` al contenedor principal
- [ ] Agregar `<div id="footer-container"></div>`
- [ ] Llamar `Navbar.checkAuth()` si es página protegida
- [ ] Inicializar navbar con `currentPage` correcto
- [ ] Inicializar footer con opciones deseadas

---

## 📚 Referencias

- **Tailwind CSS**: https://tailwindcss.com/docs
- **Feather Icons**: https://feathericons.com/
- **LocalStorage API**: https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage

---

## 📄 Ejemplo Completo

Ver archivos de referencia:
- `dashboard.html` - Ejemplo completo con navbar y footer
- `compose-email.html` - Ejemplo de página protegida
- `login.html` - Ejemplo de página pública con footer
- `index.html` - Ejemplo de landing page

---

**Última actualización:** Diciembre 2025  
**Versión:** 1.0.0  
**Mantenedor:** GitHub Copilot
