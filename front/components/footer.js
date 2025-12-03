/**
 * Footer Component - ORGSECURE
 * Componente reutilizable de pie de página para todas las páginas
 */

class Footer {
  constructor() {
    this.currentYear = new Date().getFullYear();
  }

  /**
   * Renderiza el footer en el contenedor especificado
   * @param {string} containerId - ID del contenedor donde se insertará el footer
   * @param {Object} options - Opciones de configuración
   * @param {string} options.theme - Tema del footer ('light' | 'dark')
   * @param {boolean} options.showLinks - Mostrar enlaces adicionales
   */
  render(containerId = 'footer-container', options = {}) {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`Contenedor ${containerId} no encontrado`);
      return;
    }

    const theme = options.theme || 'light';
    const showLinks = options.showLinks !== false;

    const bgClass = theme === 'dark' ? 'bg-gray-800 text-white' : 'bg-white text-gray-600';
    const borderClass = theme === 'dark' ? 'border-gray-700' : 'border-gray-200';
    const linkClass = theme === 'dark' ? 'text-gray-300 hover:text-white' : 'text-blue-600 hover:text-blue-800';

    container.innerHTML = `
      <footer class="${bgClass} border-t ${borderClass} mt-auto">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div class="flex flex-col md:flex-row justify-between items-center gap-4">
            <!-- Logo y copyright -->
            <div class="flex items-center gap-2">
              <img src="logo-p.png" alt="Logo" class="h-6 w-auto">
              <span class="text-sm">
                © ${this.currentYear} ORGSECURE. Todos los derechos reservados.
              </span>
            </div>

            ${showLinks ? this.renderLinks(linkClass) : ''}

            <!-- Información adicional -->
            <div class="text-sm text-center md:text-right">
              <p>Universidad Nacional de Colombia</p>
              <p class="text-xs mt-1 opacity-75">Sistema de Gestión Académica</p>
            </div>
          </div>
        </div>
      </footer>
    `;
  }

  /**
   * Renderiza los enlaces del footer
   */
  renderLinks(linkClass) {
    return `
      <div class="flex gap-4 text-sm">
        <a href="#" class="${linkClass} transition-colors">
          Ayuda
        </a>
        <span class="text-gray-400">|</span>
        <a href="#" class="${linkClass} transition-colors">
          Documentación
        </a>
        <span class="text-gray-400">|</span>
        <a href="#" class="${linkClass} transition-colors">
          Contacto
        </a>
        <span class="text-gray-400">|</span>
        <a href="#" class="${linkClass} transition-colors">
          Privacidad
        </a>
      </div>
    `;
  }

  /**
   * Renderiza un footer minimalista (solo copyright)
   */
  renderMinimal(containerId = 'footer-container') {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`Contenedor ${containerId} no encontrado`);
      return;
    }

    container.innerHTML = `
      <footer class="bg-white border-t border-gray-200 mt-auto">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div class="text-center text-sm text-gray-600">
            © ${this.currentYear} ORGSECURE - Universidad Nacional de Colombia
          </div>
        </div>
      </footer>
    `;
  }
}

// Exportar para uso en otros archivos
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Footer;
}
