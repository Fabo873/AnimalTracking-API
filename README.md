# AnimalTracking
Proyecto realizado para la la clase de Proyecto Integrador dentro del Tecnologico de Monterrey

## Objectivo
Herramienta de manejo de reportes de seguimiento de especies rescatadas.

## Uso de la API

### Requerimientos
-   Docker
-   Herramienta de pruebas de APIs REST

### Iniciar API
-   Asegurarse de que Docker se encuentre corriendo
-   Abrir terminal y situarse en la carpeta base de este proyecto
-   Correr el comando `docker-compose up`
-   Probar la API

### Detener API (Opcion 1)
-   Asegurarse de que Docker se encuentre corriendo
-   Abrir terminal y situarse en la carpeta base de este proyecto
-   Correr el comando `docker-compose stop`

### Detener API (Opcion 2)
-   Asegurarse de que Docker se encuentre corriendo
-   Abrir terminal donde se estan ejecutando los contenedores
-   Presionar `ctrl`+`c`

### Eliminar datos de API
*** El comando para detener la api unicamente detiene la ejecucion de los contenedores, pero estos siguen existiendo y los datos permaneceran al volver a iniciar la api. Para eliminar los datos existentes sigue los siguientes pasos.
-   Asegurarse de que Docker se encuentre corriendo
-   Abrir terminal donde se estan ejecutando los contenedores
-   Correr el comando `docker-compose down`

*** Si se ejecuta este comando mientras se estan en ejecucion los contenedores, primero se deteneran y luego se eliminaran los datos; so se ejecuta con los contenedores detenidos, eliminara los datos.

## Troubleshooting

### La configuracion del servidor de sql es ingorada.
Si al iniciar los contendores se percibe lo sigueinte `/etc/mysql/conf.d/custom.cnf is ignored`, esto quiere decir que la configuracion para la base de datos no se esta leyendo correctamente, esto puede desencadenar en otros problemas como que la codificacion de los caracteres de la base de datos sea erronea, o incluso que no se puedan cargar los datos de inicio por que se excedio el limite de queries. Esto no necesariamente resultara en que la construccion del contenedor se cancele, por lo que es importante estar atento a que no suceda.
Para solucionar estos problemas es necesario otorgar unicamente permiso de lectura a el archivo `/sql/mycustom.cnf`. Esto se puede lograr corriendo el siguiente comando dentro de la carpeta base del proyecto.
-   Windows -> `chmod a+rwx,u-wx,g-wx,o-wx,ug-s,-t ./sql/mycustom.cnf`
-   Linux/MacOS -> `chmod 0444 ./sql/mycustom.cnf`