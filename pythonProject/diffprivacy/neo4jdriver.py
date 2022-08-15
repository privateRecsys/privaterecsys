from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=( "neo4j", "password"))
session = driver.session()
print("create_session")


def print_greeting(self, message):
    with self.driver.session() as session:
        greeting = session.write_transaction(self._create_and_return_greeting, message)
        print(greeting)


@staticmethod
def _create_and_return_greeting(tx, message):
    result = tx.run("CREATE (a:Greeting) "
                    "SET a.message = $message "
                    "RETURN a.message + ', from node ' + id(a)", message=message)
    return result.single()[0]