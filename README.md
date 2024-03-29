# Family Tree Service

## Description

This service provide a GraphQL api for building and querying a family tree. This minimal product supports
searching for persons and their relatives(cousins, sibling, parents, grandparents, and children). It also
supports adding new person and relationship with certain limitations for simplification of the minimal 
product. It currently does not support deletes. 

## Requirements

* PyCharm - or your favorite IDE.
* Docker/Docker Compose - for running Neo4J container.
* Neo4J - included in docker-compose.yml file, a graph database. We are using the free version which
means that we do not have a full feature set and have to rely on the application for some relationship 
constraints. Which is not the most ideal layer for such constraints. 
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
  
    If you have a recent version of pip installed. So you may have to downgrade. If you get the following error you can resolve it using the following
    command:

    ```bash
    ./build.sh py37setup
    ```

    Error from higher version of pip:
    ```
      env/utils.py", line 402, in resolve_deps
        req_dir=req_dir
        File "/usr/local/lib/python3.7/site-packages/pipenv/utils.py", line 250, in actually_resolve_deps
          req = Requirement.from_line(dep)
        File "/usr/local/lib/python3.7/site-packages/pipenv/vendor/requirementslib/models/requirements.py", line 704, in from_line
          line, extras = _strip_extras(line)
      TypeError: 'module' object is not callable
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
    Any Person that has a parent relationship to another node. This is the primary relationship and it forms the
    basis for a lot of the queries we answer with the model. A parent can also be a person who is
    married to a parent. We chose this approach to account for step relationship based on marriage. 
    
    - MARRIED 
    Establishes a partnership between two persons. This is relationship put in place to give us more connectivity. 
    When two persons are married their children are counted and affects all other derived relationships. We accounted for step relationships.
    
    The following are some of the derived relationships:
    - Siblings: Persons with the same parent including children of a parent's partner by marriage.
    - Parents: Parent or partner of parent.
    - Children: Direct children or children of partner by marriage.
    - Grandparents: Parent or their spouse that are parents of my parent.
    - Cousins: Children of my parents (parent and their spouse) siblings.
    
    Because we do not currently support deletion, once you are connected to a particular family
    tree you cannot have another relationship to the same tree. For the same reason you cannot
    marry someone who is currently married. This also help to avoid some circular path in the graph and to simplify
    this demo. 
    
    
## User Interface

The application use  **GRAPHIQL** interface that makes it easy to execute graphql
queries and mutations. The interface also allows you to store command by name. More 
examples are present in the file **sample_executions.txt**. The file contains both valid and invalid
queries to test the rules of our system. 

![ui](ui.png)

Sample Mutation(create):
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

Sample Query:
```
query nicole_cousins {
  cousins(email: "nicole@nicole.com") {
    email
    first_name
    last_name
    phone_number
    address
    birthday
  }
}
```

Sample Error:
 ```json
{
  "errors": [
    {
      "message": "drew@drew.com and marcus@marcus.com are in the same family tree",
      "locations": [
        {
          "line": 74,
          "column": 3
        }
      ],
      "path": [
        "add_relationship"
      ]
    }
  ],
  "data": {
    "add_relationship": null
  }
}

```
 
 ## Future Improvements
 
 * More testing for edge cases and bad data states. With graphs there are bound to
 be edges that are not allowed. 
 * Review relationship definition and ensure that the integrity of the model is 
 preserved.
 * Add delete capability to allow for relationship corrections especially when valid relationships
 are rejected. 
  
 

