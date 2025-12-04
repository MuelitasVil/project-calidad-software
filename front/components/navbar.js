/**
 * Navbar Component - ORGSECURE
 * Componente reutilizable de navegación para todas las páginas
 */

class Navbar {
  constructor() {
    this.token = localStorage.getItem('authToken');
    let userStr = localStorage.getItem('user') || '{}';
    
    // Manejar diferentes formatos de usuario
    try {
      // Si el string empieza con comillas, es un string JSON que contiene un string
      // Ejemplo: '"mhoyos@example.com"' o '{"email":"user@example.com"}'
      const parsed = JSON.parse(userStr);
      
      if (typeof parsed === 'string') {
        // Era un string dentro de JSON, crear objeto
        this.user = { email: parsed, username: parsed };
      } else if (typeof parsed === 'object' && parsed !== null) {
        // Ya es un objeto JSON válido
        this.user = parsed;
      } else {
        // Caso inesperado, usar valor por defecto
        this.user = { email: 'Usuario', username: 'Usuario' };
      }
    } catch (e) {
      // No es JSON válido, tratarlo como string directo
      // Remover comillas si las tiene
      const cleanStr = userStr.replace(/^["']|["']$/g, '');
      this.user = { email: cleanStr, username: cleanStr };
    }
  }

  /**
   * Renderiza el navbar en el contenedor especificado
   * @param {string} containerId - ID del contenedor donde se insertará el navbar
   * @param {Object} options - Opciones de configuración
   * @param {string} options.currentPage - Página actual ('dashboard' | 'compose-email' | 'profile')
   */
  render(containerId = 'navbar-container', options = {}) {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`Contenedor ${containerId} no encontrado`);
      return;
    }

    const currentPage = options.currentPage || 'dashboard';
    const isAdmin = this.user.type_user && this.user.type_user.toLowerCase() === 'admin';
    
    container.innerHTML = `
      <nav class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <!-- Logo y título -->
            <a href="home.html" class="flex items-center gap-2 hover:opacity-80 transition-opacity">
              <img src="logo-p.png" alt="Logo" class="h-8 w-auto">
              <span class="text-xl font-semibold text-gray-800">ORGSECURE</span>
            </a>

            <!-- Usuario y acciones -->
            <div class="flex items-center gap-4">
              <!-- Display de usuario -->
              <div class="flex items-center gap-2">
                <div class="flex items-center gap-2 bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                  <i data-feather="user" class="h-4 w-4"></i>
                  <span>${this.user.username || this.user.email || 'Usuario'}</span>
                </div>
                
                <!-- Rol del usuario -->
                ${this.user.type_user ? `
                  <div class="flex items-center gap-1 bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                    <i data-feather="shield" class="h-4 w-4"></i>
                    <span>${this.user.type_user}</span>
                  </div>
                ` : ''}
              </div>

              <!-- Menú Hamburguesa -->
              <div class="relative">
                <button id="hamburgerBtn" class="text-gray-500 hover:text-gray-700 p-2 rounded-md hover:bg-gray-100 transition-colors">
                  <i data-feather="menu" class="h-6 w-6"></i>
                </button>

                <!-- Dropdown Menu -->
                <div id="dropdownMenu" class="hidden absolute right-0 mt-2 w-56 bg-white rounded-md shadow-lg border border-gray-200 z-50">
                  <div class="py-1">
                    ${this.renderMenuItems(isAdmin, currentPage)}
                  </div>
                </div>
              </div>

              <!-- Botón de logout -->
              <button id="logoutBtn" class="text-gray-500 hover:text-gray-700 flex items-center gap-1 transition-colors">
                <i data-feather="log-out" class="h-4 w-4"></i>
                <span>Salir</span>
              </button>
            </div>
          </div>
        </div>
      </nav>
    `;

    // Inicializar iconos de Feather
    if (typeof feather !== 'undefined') {
      feather.replace();
    }

    // Configurar event listeners
    this.setupEventListeners(currentPage);
  }

  /**
   * Renderiza los items del menú según el rol del usuario
   * @param {boolean} isAdmin - Si el usuario es administrador
   * @param {string} currentPage - Página actual
   */
  renderMenuItems(isAdmin, currentPage) {
    const menuItems = [];
    
    // Todos los roles ven: Inicio
    menuItems.push({
      id: 'menu-home',
      icon: 'home',
      label: 'Inicio',
      href: 'home.html',
      active: currentPage === 'home'
    });
    
    if (isAdmin) {
      // Admin ve: Correo, Usuarios, Períodos, Perfil
      menuItems.push({
        id: 'menu-compose-email',
        icon: 'mail',
        label: 'Correo',
        href: 'compose-email.html',
        active: currentPage === 'compose-email'
      });
      
      menuItems.push({
        id: 'menu-users',
        icon: 'users',
        label: 'Usuarios',
        href: 'users.html',
        active: currentPage === 'users'
      });
      
      menuItems.push({
        id: 'menu-periods',
        icon: 'calendar',
        label: 'Períodos',
        href: 'dashboard.html',
        active: currentPage === 'dashboard'
      });
    }
    
    // Todos los roles ven: Perfil
    menuItems.push({
      id: 'menu-profile',
      icon: 'user',
      label: 'Perfil',
      href: 'profile.html',
      active: currentPage === 'profile'
    });

    return menuItems.map(item => `
      <a href="${item.href}" 
         id="${item.id}"
         class="flex items-center gap-3 px-4 py-2 text-sm ${
           item.active 
             ? 'bg-blue-50 text-blue-600 font-medium' 
             : 'text-gray-700 hover:bg-gray-50'
         } transition-colors">
        <i data-feather="${item.icon}" class="h-4 w-4"></i>
        <span>${item.label}</span>
      </a>
    `).join('');
  }

  /**
   * Renderiza el botón de navegación según la página actual
   * @deprecated - Reemplazado por menú hamburguesa
   */
  renderNavigationButton(currentPage) {
    if (currentPage === 'dashboard') {
      return `
        <button id="navActionBtn" class="text-blue-600 hover:text-blue-800 flex items-center gap-1 transition-colors">
          <i data-feather="mail" class="h-4 w-4"></i>
          <span>Correo</span>
        </button>
      `;
    } else if (currentPage === 'compose-email') {
      return `
        <button id="navActionBtn" class="text-blue-600 hover:text-blue-800 flex items-center gap-1 transition-colors">
          <i data-feather="calendar" class="h-4 w-4"></i>
          <span>Períodos</span>
        </button>
      `;
    }
    return '';
  }

  /**
   * Configura los event listeners del navbar
   */
  setupEventListeners(currentPage) {
    // Toggle del menú hamburguesa
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const dropdownMenu = document.getElementById('dropdownMenu');
    
    if (hamburgerBtn && dropdownMenu) {
      hamburgerBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdownMenu.classList.toggle('hidden');
      });

      // Cerrar menú al hacer click fuera
      document.addEventListener('click', (e) => {
        if (!hamburgerBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
          dropdownMenu.classList.add('hidden');
        }
      });

      // Cerrar menú al hacer click en un item
      const menuItems = dropdownMenu.querySelectorAll('a');
      menuItems.forEach(item => {
        item.addEventListener('click', () => {
          dropdownMenu.classList.add('hidden');
        });
      });
    }

    // Botón de logout
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', () => {
        if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
          localStorage.removeItem('authToken');
          localStorage.removeItem('user');
          window.location.href = 'login.html';
        }
      });
    }
  }

  /**
   * Verifica si el usuario está autenticado
   * Redirige a login si no hay token
   */
  static checkAuth() {
    const token = localStorage.getItem('authToken');
    if (!token) {
      window.location.href = 'login.html';
      return false;
    }
    return true;
  }
}

// Exportar para uso en otros archivos
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Navbar;
}
