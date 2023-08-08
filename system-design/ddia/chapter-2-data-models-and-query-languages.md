# Data Models and Query Languages

## Document DB

Json representation.

Example:

* MongoDB
* CouchDB
* RethinkDB, Espresso etc.

## SQL vs NoSQL Database

| SQL                                                | NoSQL                                                 |
| -------------------------------------------------- | ----------------------------------------------------- |
| Better join support                                | Limited join support                                  |
| normalized structure                               | denormalized structure with locality                  |
| <p>Many-to-many<br>Many-to-one<br>relationship</p> | one-to-many relationship                              |
| XML schema with validation                         | <p>Document-like structure<br>Json representation</p> |
| Schema on write                                    | Schema on read                                        |

### Glossary

<mark style="color:blue;">Normalization</mark>: process of breaking down data into separate tables to minimize redundancy. This approach is effective for many-to-many relationship.

## Graph DB

If many-to-many relationship are very common and complex in your application, it's natural to start modeling data as graph.

Think of a graph store as two relational tables, one for vertices and one for edges.

### Examples

Property graph model: Neo4j, Titan, InfiniteGraph

Triple-store model: Datomic, AllegroGraph

Imperative graph: Gremlin, Pregel.

## Query languages:

<mark style="color:blue;">Relational DB</mark>: SQL

<mark style="color:blue;">Document DB</mark>: MapReduce, MongoDB's aggregation pipeline

<mark style="color:blue;">Graph DB</mark>: Cypher, SPARQL, Datalog
