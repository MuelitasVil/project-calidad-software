/**
 * Users Manager - Gestión de usuarios
 * Maneja registro, listado, edición y eliminación de usuarios
 */

const AUTH_API = 'http://localhost:8000';
const USERS_API = 'http://localhost:8001';
const CONTACTS_API = `${USERS_API}/contact_data`;

class UsersManager {
    constructor() {
        this.users = [];
        this.filteredUsers = [];
        this.adminContactManager = null;
        this.editContactManager = null;
        this.currentEditEmail = null;
        this.init();
    }

    init() {
        this.setupTabs();
        this.setupForms();
        this.setupSearch();
        this.initContactManager();
        this.loadUsers();
        this.updateUserCount();
    }
    
    /**
     * Actualizar contador de usuarios
     */
    async updateUserCount() {
        try {
            console.log('Fetching user count from:', `${USERS_API}/users_unal`);
            const response = await fetch(`${USERS_API}/users_unal`);
            console.log('Response status:', response.status);
            
            if (response.ok) {
                const users = await response.json();
                console.log('Total users received:', users.length);
                console.log('Users data:', users);
                
                const countElement = document.getElementById('totalUsersCount');
                console.log('Count element found:', countElement);
                
                if (countElement) {
                    countElement.textContent = users.length;
                    console.log('Updated count element to:', users.length);
                } else {
                    console.error('Element totalUsersCount not found in DOM');
                }
            } else {
                console.error('Response not ok:', response.status);
            }
        } catch (error) {
            console.error('Error al obtener el conteo de usuarios:', error);
        }
    }
    
    /**
     * Inicializar ContactManager
     */
    initContactManager() {
        this.adminContactManager = new ContactManager('adminContactsContainer', {
            showLabels: true,
            allowEmpty: true,
            minContacts: 0,
            maxContacts: 10
        });
        
        // Agregar un contacto vacío inicial
        this.adminContactManager.addContact();
        
        // Inicializar ContactManager para edición
        this.editContactManager = new ContactManager('editContactsContainer', {
            showLabels: true,
            allowEmpty: true,
            minContacts: 0,
            maxContacts: 10
        });
    }

    /**
     * Configurar navegación entre tabs
     */
    setupTabs() {
        const tabRegister = document.getElementById('tabRegister');
        const tabList = document.getElementById('tabList');
        const registerTab = document.getElementById('registerTab');
        const listTab = document.getElementById('listTab');

        const activateTab = (activeButton, activeContent) => {
            // Reset all tabs
            [tabRegister, tabList].forEach(tab => {
                tab.classList.remove('active', 'border-blue-600', 'text-blue-600');
                tab.classList.add('border-transparent', 'text-gray-500');
            });
            [registerTab, listTab].forEach(content => {
                content.classList.add('hidden');
            });

            // Activate selected tab
            activeButton.classList.add('active', 'border-blue-600', 'text-blue-600');
            activeButton.classList.remove('border-transparent', 'text-gray-500');
            activeContent.classList.remove('hidden');
            
            feather.replace();
        };

        tabRegister.addEventListener('click', () => activateTab(tabRegister, registerTab));
        tabList.addEventListener('click', () => activateTab(tabList, listTab));
    }

    /**
     * Configurar formularios
     */
    setupForms() {
        // Register form
        const registerForm = document.getElementById('registerForm');
        registerForm.addEventListener('submit', (e) => this.handleRegister(e));

        // Edit form
        const editForm = document.getElementById('editForm');
        editForm.addEventListener('submit', (e) => this.handleEdit(e));

        // Refresh button
        const refreshBtn = document.getElementById('refreshBtn');
        refreshBtn.addEventListener('click', () => this.loadUsers());

        // Modal controls
        const closeModal = document.getElementById('closeModal');
        const cancelEdit = document.getElementById('cancelEdit');
        
        closeModal.addEventListener('click', () => this.closeEditModal());
        cancelEdit.addEventListener('click', () => this.closeEditModal());
    }

    /**
     * Configurar búsqueda
     */
    setupSearch() {
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            this.filterUsers(query);
        });
    }

    /**
     * Registrar usuario en auth y users service
     */
    async handleRegister(e) {
        e.preventDefault();

        const formData = {
            e_mail: document.getElementById('email_unal').value,
            password: document.getElementById('password').value,
            type_user: document.getElementById('type_user').value,
            email_unal: document.getElementById('email_unal').value,
            document: document.getElementById('document').value || null,
            name: document.getElementById('name').value || null,
            lastname: document.getElementById('lastname').value || null,
            full_name: document.getElementById('full_name').value || null,
            gender: document.getElementById('gender').value || null,
            birth_date: document.getElementById('birth_date').value || null
        };
        
        // Obtener contactos del manager
        const contacts = this.adminContactManager.getContacts();

        try {
            // Show loading
            const submitBtn = e.target.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i data-feather="loader" class="h-5 w-5 animate-spin"></i> Registrando...';
            feather.replace();

            // 1. Register in Auth service
            const authResponse = await fetch(`${AUTH_API}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    e_mail: formData.e_mail,
                    password: formData.password,
                    type_user: formData.type_user
                })
            });

            if (!authResponse.ok) {
                const error = await authResponse.json();
                throw new Error(error.detail || 'Error en registro de autenticación');
            }

            // 2. Register in Users service
            const usersResponse = await fetch(`${USERS_API}/users_unal/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email_unal: formData.email_unal,
                    document: formData.document,
                    name: formData.name,
                    lastname: formData.lastname,
                    full_name: formData.full_name,
                    gender: formData.gender,
                    birth_date: formData.birth_date
                })
            });

            if (!usersResponse.ok) {
                const error = await usersResponse.json();
                throw new Error(error.detail || 'Error en registro de usuario');
            }

            // 3. Create contact data (array of contacts)
            if (contacts.length > 0) {
                const contactsWithEmail = contacts.map(c => ({
                    ...c,
                    email_unal: formData.email_unal
                }));
                
                const contactResponse = await fetch(`${CONTACTS_API}/bulk`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(contactsWithEmail)
                });

                if (!contactResponse.ok) {
                    console.warn('Warning: Contact data not saved, but user was created');
                }
            }

            // Success
            this.showNotification('Usuario registrado exitosamente', 'success');
            document.getElementById('registerForm').reset();
            this.adminContactManager.clear();
            this.adminContactManager.addContact();
            
            // Update user count
            this.updateUserCount();
            
            // Switch to list tab
            document.getElementById('tabList').click();

        } catch (error) {
            console.error('Error:', error);
            this.showNotification(error.message, 'error');
        } finally {
            // Restore button
            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i data-feather="save" class="h-5 w-5"></i><span>Registrar Usuario</span>';
            feather.replace();
        }
    }

    /**
     * Cargar lista de usuarios
     */
    async loadUsers() {
        const tbody = document.getElementById('usersTableBody');
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                    <i data-feather="loader" class="inline h-5 w-5 animate-spin"></i>
                    Cargando usuarios...
                </td>
            </tr>
        `;
        feather.replace();

        try {
            const response = await fetch(`${USERS_API}/users_unal/`);
            
            if (!response.ok) {
                throw new Error('Error al cargar usuarios');
            }

            this.users = await response.json();
            
            // Obtener roles de cada usuario
            await this.loadUserRoles();
            
            this.filteredUsers = [...this.users];
            this.renderUsers();

        } catch (error) {
            console.error('Error:', error);
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="px-6 py-4 text-center text-red-500">
                        <i data-feather="alert-circle" class="inline h-5 w-5"></i>
                        Error al cargar usuarios: ${error.message}
                    </td>
                </tr>
            `;
            feather.replace();
        }
    }

    /**
     * Cargar roles de usuarios desde auth service
     */
    async loadUserRoles() {
        for (let user of this.users) {
            try {
                const response = await fetch(`${AUTH_API}/auth/user/${user.email_unal}/type`);
                if (response.ok) {
                    const data = await response.json();
                    user.type_user = data.type_user;
                } else {
                    user.type_user = 'guest'; // Default
                }
            } catch (error) {
                console.error(`Error getting role for ${user.email_unal}:`, error);
                user.type_user = 'guest';
            }
        }
    }

    /**
     * Renderizar tabla de usuarios
     */
    renderUsers() {
        const tbody = document.getElementById('usersTableBody');
        const userCount = document.getElementById('userCount');

        if (this.filteredUsers.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                        <i data-feather="inbox" class="inline h-5 w-5"></i>
                        No hay usuarios registrados
                    </td>
                </tr>
            `;
            userCount.textContent = 'Total: 0 usuarios';
            feather.replace();
            return;
        }

        // Badges de rol con colores
        const getRoleBadge = (role) => {
            const badges = {
                'admin': '<span class="px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800">Admin</span>',
                'professor': '<span class="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">Profesor</span>',
                'student': '<span class="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">Estudiante</span>',
                'guest': '<span class="px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800">Invitado</span>'
            };
            return badges[role] || badges['guest'];
        };

        tbody.innerHTML = this.filteredUsers.map(user => `
            <tr class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${user.email_unal}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${user.full_name || '-'}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${user.document || '-'}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                    ${getRoleBadge(user.type_user)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${user.gender || '-'}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div class="flex gap-2">
                        <button onclick="usersManager.editUser('${user.email_unal}')" 
                                class="text-blue-600 hover:text-blue-800">
                            <i data-feather="edit-2" class="h-4 w-4"></i>
                        </button>
                        <button onclick="usersManager.deleteUser('${user.email_unal}')" 
                                class="text-red-600 hover:text-red-800">
                            <i data-feather="trash-2" class="h-4 w-4"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');

        userCount.textContent = `Total: ${this.filteredUsers.length} usuario${this.filteredUsers.length !== 1 ? 's' : ''}`;
        feather.replace();
    }

    /**
     * Filtrar usuarios
     */
    filterUsers(query) {
        if (!query) {
            this.filteredUsers = [...this.users];
        } else {
            this.filteredUsers = this.users.filter(user => 
                user.email_unal.toLowerCase().includes(query) ||
                (user.full_name && user.full_name.toLowerCase().includes(query)) ||
                (user.document && user.document.toLowerCase().includes(query))
            );
        }
        this.renderUsers();
    }

    /**
     * Abrir modal de edición
     */
    async editUser(email) {
        const user = this.users.find(u => u.email_unal === email);
        if (!user) return;

        this.currentEditEmail = email;

        document.getElementById('edit_email_unal').value = user.email_unal;
        document.getElementById('edit_email_display').value = user.email_unal;
        document.getElementById('edit_type_user').value = user.type_user || 'guest';
        document.getElementById('edit_password').value = '';
        document.getElementById('edit_document').value = user.document || '';
        document.getElementById('edit_name').value = user.name || '';
        document.getElementById('edit_lastname').value = user.lastname || '';
        document.getElementById('edit_full_name').value = user.full_name || '';
        document.getElementById('edit_gender').value = user.gender || '';
        document.getElementById('edit_birth_date').value = user.birth_date || '';

        // Cargar contactos del usuario
        await this.loadUserContacts(email);

        document.getElementById('editModal').classList.remove('hidden');
    }

    /**
     * Cargar contactos de un usuario
     */
    async loadUserContacts(email) {
        try {
            const response = await fetch(`${CONTACTS_API}/user/${encodeURIComponent(email)}`);
            if (response.ok) {
                const contacts = await response.json();
                if (contacts.length > 0) {
                    this.editContactManager.loadContacts(contacts);
                } else {
                    // No hay contactos, agregar uno vacío
                    this.editContactManager.clear();
                    this.editContactManager.addContact();
                }
            } else {
                // Error al cargar, agregar uno vacío
                this.editContactManager.clear();
                this.editContactManager.addContact();
            }
        } catch (error) {
            console.error('Error loading contacts:', error);
            this.editContactManager.clear();
            this.editContactManager.addContact();
        }
    }

    /**
     * Cerrar modal de edición
     */
    closeEditModal() {
        document.getElementById('editModal').classList.add('hidden');
    }

    /**
     * Manejar edición de usuario
     */
    async handleEdit(e) {
        e.preventDefault();

        const email = document.getElementById('edit_email_unal').value;
        const newPassword = document.getElementById('edit_password').value.trim();
        const newTypeUser = document.getElementById('edit_type_user').value;
        
        const userUnalData = {
            email_unal: email,
            document: document.getElementById('edit_document').value || null,
            name: document.getElementById('edit_name').value || null,
            lastname: document.getElementById('edit_lastname').value || null,
            full_name: document.getElementById('edit_full_name').value || null,
            gender: document.getElementById('edit_gender').value || null,
            birth_date: document.getElementById('edit_birth_date').value || null
        };

        try {
            // 1. Actualizar en users_unal
            const usersResponse = await fetch(`${USERS_API}/users_unal/${email}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userUnalData)
            });

            if (!usersResponse.ok) {
                const error = await usersResponse.json();
                throw new Error(error.detail || 'Error al actualizar usuario');
            }

            // 2. Actualizar en auth (contraseña y/o rol) si hay cambios
            const authUpdateData = {};
            if (newPassword) {
                authUpdateData.password = newPassword;
            }
            if (newTypeUser) {
                authUpdateData.type_user = newTypeUser;
            }

            if (Object.keys(authUpdateData).length > 0) {
                const authResponse = await fetch(`${AUTH_API}/auth/user/${email}`, {
                    method: 'PATCH',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(authUpdateData)
                });

                if (!authResponse.ok) {
                    const error = await authResponse.json();
                    throw new Error(error.detail || 'Error al actualizar autenticación');
                }
            }

            // 3. Sincronizar contactos
            const contacts = this.editContactManager.getContacts();
            if (contacts.length > 0) {
                const contactResponse = await fetch(`${CONTACTS_API}/user/${encodeURIComponent(email)}/sync`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(contacts)
                });

                if (!contactResponse.ok) {
                    console.warn('Warning: Contact data not updated');
                }
            }

            this.showNotification('Usuario actualizado exitosamente', 'success');
            this.closeEditModal();
            this.loadUsers();
            this.updateUserCount();

        } catch (error) {
            console.error('Error:', error);
            this.showNotification(error.message, 'error');
        }
    }

    /**
     * Eliminar usuario
     */
    async deleteUser(email) {
        if (!confirm(`¿Estás seguro de eliminar el usuario ${email}?`)) {
            return;
        }

        try {
            const response = await fetch(`${USERS_API}/users_unal/${email}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al eliminar usuario');
            }

            this.showNotification('Usuario eliminado exitosamente', 'success');
            this.loadUsers();
            this.updateUserCount();

        } catch (error) {
            console.error('Error:', error);
            this.showNotification(error.message, 'error');
        }
    }

    /**
     * Mostrar notificación
     */
    showNotification(message, type = 'success') {
        const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';
        const icon = type === 'success' ? 'check-circle' : 'alert-circle';

        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 ${bgColor} text-white px-6 py-3 rounded-md shadow-lg z-50 flex items-center gap-2`;
        notification.innerHTML = `
            <i data-feather="${icon}" class="h-5 w-5"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        feather.replace();

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize
const usersManager = new UsersManager();
