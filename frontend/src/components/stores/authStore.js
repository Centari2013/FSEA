import { defineStore } from "pinia";
import { client } from "../../scripts/api_access/apollo_client";
import { gql } from "@apollo/client/core";

const VALIDATE_TOKEN_MUTATION = gql`
  mutation ValidateToken($token: String!) {
    validateToken(token: $token) {
      valid
    }
  }
`;

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuthenticated: false,
    loading: true, // Helps with route guards
  }),
  actions: {
    async verifyToken() {
      const token = localStorage.getItem("sessionToken");
      if (!token) {
        this.isAuthenticated = false;
        this.loading = false;
        return false;
      }

      try {
        const { data } = await client.mutate({
          mutation: VALIDATE_TOKEN_MUTATION,
          variables: { token },
        });

        if (data?.validateToken?.valid) {
          this.isAuthenticated = true;
        } else {
          this.isAuthenticated = false;
          localStorage.removeItem("sessionToken"); // Remove invalid token
        }
      } catch (error) {
        console.error("Error verifying token:", error);
        this.isAuthenticated = false;
      }

      this.loading = false;
      return this.isAuthenticated;
    },
    logout() {
      this.isAuthenticated = false;
      localStorage.removeItem("sessionToken");
      window.location.href = "/login"; // Redirect to login page
    },
  },
});
