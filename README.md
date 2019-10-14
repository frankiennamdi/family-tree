# Family Tree Service

## Description

This service provide a GraphQL api for building and querying a family tree. This minimal product supports
searching for persons and their relatives(cousins, sibling, parents, grandparents, and children). It also
supports adding new person and relationship with certain limitations for simplification of the minimal 
product. It currently does not support deletes. 

## Requirements

* PyCharm - or your favorite IDE.
* Docker/Docker Compose - for running Neo4J container.
* Neo4J - included in docker-compose.yml file, a graph database.
* Python 3.7
* Pipenv - virtual environment and dependency manager.
* Bash - scripts and command execution.

## Executions

Most required commands has been wrapped and included in the **build.sh** file 

1. **View available commands** 

    ```bash
    ./build.sh
    ```

2. **Prepare your environment** 
    
    If you have a recent version of pip installed. So you may have to downgrade

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

    For running queries and mutations.

    http://localhost:9090/api/family-tree

8. **Access the Neo4j browser** 

    For viewing the nodes and their relationships.

    http://localhost:7474/
    
## Data

### Migration:
  
  The application uses a simple migration script to migrate or execute initial set of data modification
  statements for testing purpose. For simplicity this migration is **run every time the 
  application is restarted**. Future improvement will see a storage of the version to prevent
  repeated execution especially to avoid primary key constraints. 
  
### Model

Here we define some of the assumptions we make about the data, and its semantics.
This is just a contrived model with made up data to be able to answer some of the questions about a
person's relationship and their family tree. 

1. **Person:** 
    
    A family tree is made up person nodes or entities that are connected by relationships. 
    The following are the properties of the person entity:
    - First name
    - Last name
    - Phone number
    - **Email address** Unique key
    - Address
    - Birth date

2. **Relationship:**
    
    Persons of the same family are connected by the **PARENT** and **MARRIED** relationship. Every other
    relationship in the family is derived from these two relationships.
    
    - PARENT: 
    Any Person that has a parent relationship to another node. A parent can also be a person who is
    married to a parent. We chose this approach to account for step relationship based on marriage. 
    
    - MARRIED 
    Establishes a partnership between two persons. When two persons are married their children are counted
    and affects all other derived relationships. We accounted for step relationships.
    
    The following are some of the derived relationships:
    - Siblings: Persons with the same parent including children of a parent's partner by marriage.
    - Parents: Parent or partner of parent.
    - Children: Direct children or children of partner by marriage.
    - Grandparents: Parent or their spouse that are parents my parent.
    - Cousins: Children of my parents (parent and their spouse) siblings.
    
    Because we do not currently support deletion, once you are connected to a particular family
    tree you cannot have another relationship to the same tree. For the same reason you cannot
    marry someone who is currently married. This also help to avoid some circular path in the graph.
    
    
## User Interface

The application use  **GRAPHIQL** interface that makes it easy to execute graphql
queries and mutations. The interface also allows you to store command by name. More 
examples are present in the file **sample_executions.txt**. 

    ```
    mutation create_daren {
      create_person(person_input: {
        email: "daren@daren.com"
        first_name: "Darent"
        last_name: "TheDarent"
        phone_number:"322-222-4444"
        address: "daren's home"
        birthday: "2019-10-12"
        
      }) 
      {
        updated_person {
          email
          first_name
          last_name
          phone_number
          address
          birthday
        }
        success
      }
    }
    ```
 
 ## Improvements
 
 * More testing for edge cases and bad data states. 
 * Review relationship definition and ensure that the integrity of the model is 
 preserved.
 * Add delete capability to allow for relationship corrections. 
  
 

