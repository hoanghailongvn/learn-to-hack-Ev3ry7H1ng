# [GraphQL - Introspection](https://www.root-me.org/en/Challenges/Web-Server/GraphQL-Introspection)

## Statement

Take your first steps in exploring a GraphQL schema with the introspection feature!
Who knows, you might discover something...

## Resources

- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20GraphQL%20-%20Query%20GraphQL%20-%20GraphQL.pdf>
- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20GraphQL%20%20-%20%20grahql.pdf>

## GraphQL

GraphQL is a query language for your API, and a server-side runtime for executing queries using a type system you define for your data. GraphQL isn't tied to any specific database or storage engine and is instead backed by your existing code and data.

It's often useful to ask a GraphQL schema for information about what queries it supports. GraphQL allows us to do so using the introspection system!

## Capture the flag

capture a request contains GraphQL:
![1.png](./image/GraphQL%20-%20Introspection%201.png)

follow the instructions in the introspection document

- We designed the type system, so we know what types are available, but if we didn't, we can ask GraphQL, by querying the __schema field, always available on the root type of a Query. Let's do so now, and ask what types are available:

  ```graphql
  {
    __schema {
      types {
        name
      }
    }
  }
  ```

  ![2.png](./image/GraphQL%20-%20Introspection%202.png)
  - Found a interesting result here: `IAmNotHere`
- check `IAmNotHere`:

  ```graphql
  {
    __type(name: "Droid") {
      name
      kind
    }
  }
  ```

  ![3.png](./image/GraphQL%20-%20Introspection%203.png)
- ask the introspection what fields are available:

  ```graphql
  {
    __type(name: "Droid") {
      name
      fields {
        name
        type {
          name
          kind
        }
      }
    }
  }
  ```

  ![4.png](./image/GraphQL%20-%20Introspection%204.png)
- Time to get the data:
  
  ![5.png](./image/GraphQL%20-%20Introspection%205.png)
- Oops, again:

  ![6.png](./image/GraphQL%20-%20Introspection%206.png)
- we got "n" character with `id:1`, let's use burp's intruder to get all the data:

  ![7.png](./image/GraphQL%20-%20Introspection%207.png)
  - the flag at `id:17`: 
    - `RM{1ntr0sp3ct1On_1s_us3ful}`

## References

- GraphQL:
  - <https://graphql.org/learn/>
  - <https://graphql.org/learn/introspection/>
