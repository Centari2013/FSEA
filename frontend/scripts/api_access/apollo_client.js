import { ApolloClient, gql,InMemoryCache} from "@apollo/client/core";

export const client = new ApolloClient({
    uri: import.meta.env.VITE_API_ENDPOINT,
    cache: new InMemoryCache(),
})
