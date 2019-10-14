# Family Tree Service

## Description

This service provide a GraphQL api for query and building a family tree. This minimal product support
searching for person and their relatives(cousins, sibling, parents, grandparents, and children). It also
supports adding new person and relationship with certain limitations for simplification of the minimal 
product. It currently does not support deletes. 

## Requirements

* PyCharm - or your favorite IDE
* Docker/Docker Compose - for running Neo4J container
* Neo4J - included in docker-compose.yml file
* Python 3.7
* Pipenv 
* Bash

## Executions

Most expected command has been included in the **build.sh** file 

1. **View available commands** 

    ```bash
    ./build.sh
    ```

2. **Prepare your environment** if you have a recent version of pip installed. So you may have to downgrade

    ```bash
    ./build.sh py37setup
    ```

3. **Start Neo4j container**

    In another terminal start the Neo4j database. 
    
    ```bash
    docker-compose up
    ```

4. **Install dependencies and run test** 

    ```bash
    ./build.sh install-test
    ```

5. **Continuously run test**

    ```bash
    ./build.sh test
    ```

6. **Start server**

    ```bash
    ./build.sh run-local
    ```

7. **Access the endpoint**

    For running running queries and mutations

    http://localhost:9090/api/family-tree

8. **Access the Neo4j browser** 

    For view the node and relationship

    http://localhost:7474/
    
## Data

### Migration:
  
  The application uses a simple migration script to migrate or execute an initial set of cypher
  statements for testing purpose. For simplicity this migration is run every time the 
  application is restarted. Future improvement will see a storage of the version to prevent
  repeated execution especially to avoid primary key constraints. 
  
### Model

1. **Person:** 
    
    A family tree is made up person nodes or entities that are connected by relationships. 
    The following are the properties of the person entity:
    - First name
    - Last name
    - Phone number
    - Email address
    - Address
    - Birth date

2. **Relationship:**
    
    Persons of the family are connected by the PARENT and MARRIED relationship. Every other
    relationship in the family is derived from these two relationships. 
  
 

