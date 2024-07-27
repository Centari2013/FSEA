// apollo_client.js
import { ApolloClient, InMemoryCache, HttpLink, ApolloLink, gql } from "@apollo/client/core";
import { setContext } from '@apollo/client/link/context';

const httpLink = new HttpLink({
  uri: import.meta.env.VITE_API_ENDPOINT,
});

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('sessionToken');
  const employee_id = localStorage.getItem('employee_id')
  return {
    headers: {
      ...headers,
      "x-employee-id": employee_id ? employee_id : null,
      authorization: token ? `Bearer ${token}` : "",
    },
  };
});

const link = ApolloLink.from([authLink, httpLink]);

export const client = new ApolloClient({
  link: link,
  cache: new InMemoryCache(),
});
