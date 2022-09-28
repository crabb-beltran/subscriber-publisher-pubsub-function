# DOCUMENTACION PROYECTO

Proyecto desarrollado con el fin de modificar la zona horaria de los eventos del arsaigth.

## 1. Nombre

Modificación de zona horaria y registro historico de los eventos de seguridad.

## 2. Descripción

Recibir los eventos que se activan por violación de seguridad, permitiendo capturarlos desde el topico de pubsub para su posterior almacenamiento y modificación zona horaria en bigquery, finalizando con la publicación del mensaje del evento en el topico que consume el arsaigth.

## 3. Instalación

Instalar en el entorno virtual las herramientas google y version de librerias a utilizar.

```bash
$ pip install -r app/requirements.txt
```

## 4. Despliegue Cloud Functions:

1. Creación del trigger "activador".

    1.1 Creación de bucket donde se alojan los .json generados por el log operations.

2. Creación de la service_accounts.

    2.1 Asignar permisos en los servicios.
```txt
Administrador de objetos de Storage
Publicador de mensajes en topico Pub/Sub
```

3. Creación de las Cloud Functions:

    3.1 Para el despliegue en cloud functions se utiliza la versión de python 3.10 de lo contrario no logra instalar las librerias declaradas en el archivo requirements.txt

    3.2 Subir solo los scripts usados mediante importación de librerias en el main.

    3.3 Deshabilitar la opción de reintento en caso de error.

    3.5 Usar una memoria de 512 MB.

    3.6 Usar instancias de 1 a 100.

    3.7 Usar tiempo de espera de 60 segundos.

    3.8 Usar la service_accounts habilitada para usarse en los proyectos de GCP (ver punto 2).

    3.9 Crear variables de entorno.

    ```bash
    #Path de la ubicación del json service_accounts
    export GOOGLE_APPLICATION_CREDENTIALS='C:\gcp-st-transit-multi-cloud-2594cebbd43e.json'

    export PROJECT_ID='gcp-st-transit-multi-cloud'
    export TOPIC_ID='gcp-st-tmc-top-03'
    export DATASET_ID='AuditLogOperations'
    export TABLE_ID='messages_pubsub_arsight'
    export BUCKET_IN='gcp-st-tmc-audit'
    ```

    3.10. Verificar existencia de las variables de entorno creadas:

    ```bash
    echo $NAME_EMAIL
    ```

    **Nota:** Si no se crean estas variables de entorno el sistema arrojara el siguiente error.

    ```bash
    TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'

    TypeError: str expected, not NoneType
    ```

    3.11. Verificación de registro y modificación desde Bigquery.
    ```sql
    SELECT JSON_QUERY(messages, "$.receiveTimestamp"),*
    FROM `gcp-st-transit-multi-cloud.AuditLogOperations.messages_pubsub_arsight`

    DELETE FROM `gcp-st-transit-multi-cloud.AuditLogOperations.messages_pubsub_arsight` WHERE flag >=0
    ```

## 4. Lógica del Desarrollo:

*./app/main*

Este scrypt cumple con la función de orquestar las funciones desarrollada en los demás scripts.
En primer lugar genera la declaración e iniciación de las variables globales mediante variables de entorno o inicialización vacia. Como primera función llama a Starting procces para comenzar a instanciar el scrypt de listar objetos del bucket indicado y asi este nos retorna los objetos que recorremos 1 a 1 y le generamos la respectiva lectura y encode para poder tratar la cadena de string como una cadena de json. Una vez listo el mensaje se agrega a un array hasta recorrer todos los objetos y poder realizar la respectiva inserción en el dataframe, en donde agregamos la fecha y hora de manipulación y la marcación del flag segun las siguientes definiciones:

* Flag = 0 Corresponde al mensaje original insertado en bigquery
* Flag = 1 Corresponde al mensaje modificado en su hora en bigquery.
* Flag = 2 Corresponde al mensaje publicado en el topico que consume el arsight.

Teniendo listo el dataframe es invocada la función de inserción del script bigquery_functions. Luego es invocada la función de actualización que se encarga de editar la zona horaria del mensaje, y luego se invoca la función de selección a capturando unicamente los eventos con flag 1 que se encuentran listos para ser publicados en el topico.

Si la publicación en el topico es exitosa el mensaje en bigquery es marcado con flag 2 indicando correcta publicaión y se imprime el puclisher_id y finaliza el proceso.

**Nota:** Este scrypt en el despliegue de la cloud functions debe remplazarce por *main.py* y con punto de entrada *main*.

## 5. Roadmap - Ideas
* [x] Realizar un desarrollo con programación orientada a objetos.

* [ ] Generar integración para pruebas unitarias.

## 6. Autor
Cristian Beltrán -- Data Engineer

## 7. Referencias
> Pub/Sub (2022). [cloud.google.com](https://cloud.google.com/pubsub?hl=es-419)
> Pub/Sub Publisher (2022). [cloud.google.com](https://cloud.google.com/pubsub/docs/publisher)

## 8. Estado del Proyecto - Fases Devops
* [x] Fase de Planeación (Entendimiento del brief. Roadmap)
* [x] Fase de Construcción (Generación de Diseño y Código del desarrollo)
* [x] Fase de Integración Continua (Testeo, calidad con sonar. Pruebas unitarias)
* [ ] Fase de Implementación o Despliegue continuo (Instalación en los ambientes qa, staging, production con github actions)
* [ ] Fase de Gestionar
* [ ] Fase de Feedback Continuo (Retroalimentación Cliente y Usuario)