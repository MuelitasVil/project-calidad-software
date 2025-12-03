Requisitos Funcionales (RF)
RF1. Autenticación de usuarios
* RF1.1. El sistema debe permitir el inicio de sesión mediante una página de login. -->OK
* RF1.2. El login debe permitir el acceso tanto a usuarios normales como al usuario administrador.-->OK
* RF1.3. El sistema debe permitir contraseñas simples (a solicitud del cliente), sin requerir reglas estrictas de seguridad.
* RF1.4. El administrador debe acceder con una única cuenta especial de administración.-->OK

RF2. Gestión de usuarios
* RF2.1. El sistema debe permitir registrar usuarios nuevos de manera individual.-->OK
* RF2.2. El sistema debe permitir almacenar para cada usuario: Nombre completo, Uno o dos correos electrónicos (institucional y personal), Número de teléfono, Placa de vehículo y Rol del usuario (estudiante, profesor, invitado)
* RF2.3. El usuario debe poder editar sus propios datos: Correo electrónico, Número de teléfono, Placa del vehículo
* RF2.4. El administrador debe poder: Crear usuarios, Editar la información de cualquier usuario, Actualizar correo y contraseña, Clasificar usuarios según rol-->OK

RF3. Consulta y búsqueda de usuarios
* RF3.1. El administrador debe poder buscar usuarios por: Correo electrónico, Cedula, Nombre
* RF3.2. El administrador debe poder visualizar el número total de usuarios registrados mediante un indicador grande y visible.

RF4. Interfaz del sistema (Front-end)
RF4.1. El sistema debe contar con un front-end funcional.
RF4.2. La interfaz debe utilizar un color púrpura claro, acorde al nuevo estilo visual solicitado por la Universidad.
RF4.3. La interfaz debe permitir navegar entre: Login, Gestión de usuarios, Envío de notificaciones, Estadísticas (número de usuarios)

Requisitos No Funcionales (RNF)
RNF1. Rendimiento
* RNF1.1. El sistema debe tener tiempos de respuesta rápidos, evitando demoras perceptibles por el usuario.
* RNF1.2. La carga de usuarios debe completarse sin fallos y en un tiempo razonable.

RNF2. Usabilidad
* RNF2.1. La interfaz debe ser simple, clara y entendible para usuarios sin conocimientos técnicos.
* RNF2.2. La edición de datos debe ser intuitiva para evitar complicaciones.
* RNF2.3. El login debe ser fácil de usar, especialmente pensado para personal administrativo que no maneja contraseñas complejas.

RNF3. Seguridad
* RNF3.1. Aunque el cliente solicita contraseñas simples, el sistema debe implementar medidas mínimas de seguridad, se sugiere la implementación de un OTP.
* RNF3.2. Acceso único al rol administrador.




---------------------------
Requerimientos : Dos tipos de roles, normal (estudiantes,profesores), administrador señora 50 años,,,,,Usuarios normales pueden editar su propio usuario : 2 correos, teléfono, placa vehículo si tiene,,,,,Usuario administrador, puede visualizar,editar,buscar,agregar usuarios normales además puede ver el número de usuarios agregados,,,,Seguridad: que sea rápido y fácil ingresar :OTP,,,,,No funcional cambiar colores de front a púrpura claro y que el sistema sea rápido