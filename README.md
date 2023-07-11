# Lipid Genomic Metabolic Models Annotator Lipid_GEMA
### Description 

One of the key challenges in lipid analysis is the absence of comprehensive annotations for GSM models with defined structural representations. This gap limits the ability to validate and correlate experimental data with the lipid models under investigation. Lipid_GEMA aims to overcome this hurdle by offering a powerful annotation framework tailored specifically for these models.

Lipid_GEMA is a powerful annotation tool designed to streamline lipid analysis and annotation processes. Built with a comprehensive database utilizing Lipid Maps and Swiss Lipids information, this tool combines python algorithm with extensive lipid knowledge to provide accurate and efficient annotations.
At his core lies a robust graph database meticulously constructed to store a complex collection of lipid data. Leveraging the rich resources provided by Lipid Maps and Swiss Lipids, the database emcompasses a wide range of lipid entities, ensure comprehensive coverage across various lipid classes, subtypes, and structural variations. 

The Python pipeline employed by Lipid_GEMA serves as a critical component, enabling seamless connectivity between the user and the database. Through advanced matching techniques, the algorithm efficiently identifies and retrieves relevant lipid information from the database. Moreover this information is used to perform the annotation of structurally defined lipids facilitating accurate mapping and validation of lipidomics data. 

### Features:
- Database Integration
- Comprehensive Lipid Coverage
- Efficient Annotation Workflow

# Set-up

Lipid-GEMA can be acessed remotly or recreated in your local machine. For the last one the following steps need to be fulfill.

Necessary software:
- Docker
- Python
- Git

## Setup database

Firstly it is necessary to clone this repository. Create, or navigate folder to your choice in the command line and paste this command.

```bash
git clone https://github.com/AdrianoSilva19/Lipid_GEM.git
```
Navigate to the Database subdirectory inside the Lipid_GEM folder, or open the whole project in a IDE of your choice. Now you need to download the backup files from the original database to create a local copy. Here is the link to get the files: ??

Now we need to create and populate the Lipid_GEMA database. To create the database we only need to build and run Docker container defined in the docker-compose. 

```bash
docker-compose build

docker-compose up -d 
```

Then the database needs to be shut-down to allow the restoration of the backup files. 
In linux command line use the following code:
```bash
docker-compose down

docker run --rm -v $(pwd):/backup -v /Lipid_GEM:/data debian:jessie bash -c "cd /data && tar xvf /backup/backup.tar --strip 1"

docker-compose up -d 
```

For windows command line:
```bash
docker-compose down

docker run --rm -v %cd%:/backup -v /Lipid_GEM:/data debian:jessie bash -c "cd /data && tar xvf /backup/backup.tar --strip 1"

docker-compose up -d 
```

With the restarting of the docker container a local copy of Lipid_GEM will be created. To confirm this one can acess the logs of the container and check if the remote neo4j interface is acessible in http://localhost:747/ were the user is "neo4j" and the password "1234". In this interface  it should be possible acess all Lipid_GEMA database as represented in the screenshot. 

![alt text](neo4j_Lipid_GEMA.png "")

## Run Annotator algorithm

Now that the database container is working it is possible to activate the Annotator algorithm. To activate the code_container it is necessary to restart the code container created by the docker-compose up command.

```bash
docker start database_code_container_1 
```

Annotated models will be presented in the Annotation/models/models_annotated. 


