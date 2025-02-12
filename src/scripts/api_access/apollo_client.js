import { ApolloClient, InMemoryCache } from "@apollo/client";

export const client = new ApolloClient({
    uri: __API_URL__,
    cache: new InMemoryCache(),
    headers: {
        "employee_id": localStorage.getItem("employee_id") || "default-id"
    }
})
