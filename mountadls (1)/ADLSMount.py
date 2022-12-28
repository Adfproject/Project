# Databricks notebook source
#Python code to mount the ADLS Gen2 Storage Account from my Azure Databricks using Service Principal

# COMMAND ----------

# Define the variable sto be used for creating the connection string

# COMMAND ----------

adlsAccountName = "aholdtraining"
adlsContainerName = "raw"
aldsFolderName = "input"
mountPoint = "/mnt/input"

# COMMAND ----------

mountPoint

# COMMAND ----------

# Application(ClientID) from KeyVault

applicationId = dbutils.secrets.get(scope="hpi",key="ClientID")

# COMMAND ----------

# Application (client) Secret Key

authenticationKey = dbutils.secrets.get(scope="hpi",key="ClientSecret")

# COMMAND ----------

# Directory (Tenant) ID

tenantId = dbutils.secrets.get(scope="hpi",key="TenantID")

# COMMAND ----------

endpoint = "https://login.microsoftonline.com/" + tenantId + "/oauth2/token"

# COMMAND ----------

endpoint

# COMMAND ----------

source = "abfss://" + adlsContainerName + "@" + adlsAccountName + ".dfs.core.windows.net/" + aldsFolderName

# COMMAND ----------

source

# COMMAND ----------

# Connecting to the ADLS Storage using Service Pricipal and OAuth

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
            "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": applicationId,
           "fs.azure.account.oauth2.client.secret": authenticationKey,
           "fs.azure.account.oauth2.client.endpoint": endpoint
}

# COMMAND ----------

configs

# COMMAND ----------

#Mount ADLs Storage to DBFS 

# COMMAND ----------

mountPoint

# COMMAND ----------



# COMMAND ----------

if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
    dbutils.fs.mount(
        source = source,
        mount_point = mountPoint,
        extra_configs = configs
    )

# COMMAND ----------

# MAGIC %fs ls "mnt/input"

# COMMAND ----------


