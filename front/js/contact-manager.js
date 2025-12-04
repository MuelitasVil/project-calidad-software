/**
 * ContactManager - Componente para gestionar múltiples datos de contacto
 * Permite agregar, editar y eliminar contactos dinámicamente
 */
class ContactManager {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.contacts = [];
        this.nextTempId = 1; // Para IDs temporales antes de guardar en BD
        
        // Opciones configurables
        this.options = {
            showLabels: options.showLabels !== false,
            allowEmpty: options.allowEmpty !== false,
            minContacts: options.minContacts || 0,
            maxContacts: options.maxContacts || 10,
            ...options
        };
        
        this.render();
    }

    /**
     * Renderiza el componente completo
     */
    render() {
        this.container.innerHTML = `
            <div class="space-y-4">
                <div class="flex justify-between items-center">
                    <h3 class="text-lg font-medium text-gray-900">Datos de Contacto</h3>
                    <button type="button" 
                            id="addContactBtn"
                            class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                        <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                        </svg>
                        Agregar Contacto
                    </button>
                </div>
                
                <div id="contactsList" class="space-y-3">
                    ${this.renderContactsList()}
                </div>
                
                ${this.contacts.length === 0 ? this.renderEmptyState() : ''}
            </div>
        `;

        this.attachEventListeners();
    }

    /**
     * Renderiza la lista de contactos
     */
    renderContactsList() {
        if (this.contacts.length === 0) {
            return '';
        }

        return this.contacts.map((contact, index) => `
            <div class="contact-item border border-gray-300 rounded-lg p-4 bg-white shadow-sm" data-index="${index}">
                <div class="flex justify-between items-start mb-3">
                    <span class="text-sm font-medium text-gray-700">Contacto ${index + 1}</span>
                    <button type="button" 
                            class="remove-contact text-red-600 hover:text-red-800"
                            data-index="${index}">
                        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        ${this.options.showLabels ? '<label class="block text-sm font-medium text-gray-700 mb-1">Email Personal</label>' : ''}
                        <input type="email" 
                               class="contact-email shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md" 
                               placeholder="email@example.com"
                               value="${contact.personal_email || ''}"
                               data-index="${index}">
                    </div>
                    
                    <div>
                        ${this.options.showLabels ? '<label class="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>' : ''}
                        <input type="tel" 
                               class="contact-phone shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md" 
                               placeholder="3001234567"
                               value="${contact.phone_number || ''}"
                               data-index="${index}">
                    </div>
                    
                    <div>
                        ${this.options.showLabels ? '<label class="block text-sm font-medium text-gray-700 mb-1">Placa Vehículo</label>' : ''}
                        <input type="text" 
                               class="contact-plate shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md" 
                               placeholder="ABC123"
                               value="${contact.vehicle_plate || ''}"
                               data-index="${index}">
                    </div>
                </div>
            </div>
        `).join('');
    }

    /**
     * Renderiza el estado vacío
     */
    renderEmptyState() {
        return `
            <div class="text-center py-6 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
                <p class="mt-2 text-sm text-gray-600">No hay datos de contacto registrados</p>
                <p class="text-xs text-gray-500">Haz clic en "Agregar Contacto" para comenzar</p>
            </div>
        `;
    }

    /**
     * Adjunta event listeners
     */
    attachEventListeners() {
        // Botón agregar contacto
        const addBtn = this.container.querySelector('#addContactBtn');
        if (addBtn) {
            addBtn.addEventListener('click', () => this.addContact());
        }

        // Botones eliminar contacto
        this.container.querySelectorAll('.remove-contact').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = parseInt(e.currentTarget.dataset.index);
                this.removeContact(index);
            });
        });

        // Inputs de contactos para actualizar datos
        this.container.querySelectorAll('.contact-email, .contact-phone, .contact-plate').forEach(input => {
            input.addEventListener('input', (e) => {
                const index = parseInt(e.target.dataset.index);
                this.updateContactField(index, e.target);
            });
        });
    }

    /**
     * Agrega un nuevo contacto vacío
     */
    addContact() {
        if (this.contacts.length >= this.options.maxContacts) {
            alert(`No puedes agregar más de ${this.options.maxContacts} contactos`);
            return;
        }

        this.contacts.push({
            tempId: this.nextTempId++,
            personal_email: '',
            phone_number: '',
            vehicle_plate: ''
        });

        this.render();
    }

    /**
     * Elimina un contacto por índice
     */
    removeContact(index) {
        if (this.contacts.length <= this.options.minContacts) {
            alert(`Debes mantener al menos ${this.options.minContacts} contacto(s)`);
            return;
        }

        this.contacts.splice(index, 1);
        this.render();
    }

    /**
     * Actualiza un campo de un contacto
     */
    updateContactField(index, input) {
        const contact = this.contacts[index];
        if (!contact) return;

        if (input.classList.contains('contact-email')) {
            contact.personal_email = input.value;
        } else if (input.classList.contains('contact-phone')) {
            contact.phone_number = input.value;
        } else if (input.classList.contains('contact-plate')) {
            contact.vehicle_plate = input.value;
        }
    }

    /**
     * Carga contactos existentes (desde API)
     */
    loadContacts(contacts) {
        this.contacts = contacts.map(c => ({
            id: c.id,
            personal_email: c.personal_email || '',
            phone_number: c.phone_number || '',
            vehicle_plate: c.vehicle_plate || ''
        }));
        this.render();
    }

    /**
     * Obtiene los contactos actuales validados
     */
    getContacts() {
        // Filtrar contactos que tengan al menos un campo lleno
        return this.contacts.filter(contact => {
            return contact.personal_email || contact.phone_number || contact.vehicle_plate;
        }).map(contact => {
            const result = {};
            if (contact.id) result.id = contact.id;
            if (contact.personal_email) result.personal_email = contact.personal_email;
            if (contact.phone_number) result.phone_number = contact.phone_number;
            if (contact.vehicle_plate) result.vehicle_plate = contact.vehicle_plate;
            return result;
        });
    }

    /**
     * Valida que haya al menos un contacto con datos
     */
    validate() {
        const validContacts = this.getContacts();
        
        if (!this.options.allowEmpty && validContacts.length === 0) {
            return {
                valid: false,
                message: 'Debes agregar al menos un dato de contacto'
            };
        }

        if (validContacts.length < this.options.minContacts) {
            return {
                valid: false,
                message: `Debes agregar al menos ${this.options.minContacts} contacto(s)`
            };
        }

        return { valid: true };
    }

    /**
     * Limpia todos los contactos
     */
    clear() {
        this.contacts = [];
        this.render();
    }
}
