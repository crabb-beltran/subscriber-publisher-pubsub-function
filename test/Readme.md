# DOCUMENTACION PROYECTO :dart::octocat:

Proyecto desarrollado con el fin de modernizar la trasferencia de archivos mediante la integración multicloud hacia los diferentes frentes de negocio configurados.

## 1. Nombre :computer:

Exportación de datos.

## 2. Descripción 	:bookmark_tabs:

Este proyecto tiene como objetivo realizar la transferencia de información mediante el uso del desarrollo de integración multicloud, este desarrollo de export data es generada mediante python y pyspark.

## 3. Instalación :jigsaw:

    4.9 Crear variables de entorno.

    ```bash
    #path de la ubicación del json service_accounts
    export GOOGLE_APPLICATION_CREDENTIALS='C:\Users\crist\OneDrive\Escritorio\Proyectos\BdB\service_accounts\sa_cds_st_idt_export_fields_v-env-6.json'

    export PROJECT_ID='bdb-gcp-st-cds-idt'
    export DATASET_ID='quality'
    export TABLE_PARAMETERS='export_parameters'

    export BUCKET_IN='bdb-gcp-cds-st-dictionary-zone'
    export FILE_DICTIONARY='Diccionario_ADL.xlsx'
    export SHEET='fct_maestro_ventas'
    export SOURCE='fct_maestro_ventas'

    export BUCKET_OUT='bdb-gcp-cds-st-transient-zone' #--'bdb-gcp-qa-transient-zone' #Solicitar permiso a la service_accounts
    export BUCKET_DEST='bdb-gcp-st-cds-idt-export-zone' #does not have storage.objects.create access to the Google Cloud Storage object.
    export CLIENT='export-adl'
