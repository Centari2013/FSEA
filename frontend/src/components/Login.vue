<template>
    <div class="login-form-container h-full w-full rounded-xl shadow shadow-black flex flex-col justify-center items-center space-y-4">
        <img src="../assets/fsea_logo.png" alt="FSEA Logo" class="form-logo">
        <div id="loginForm" class="space-y-4">
            <div class="form-group flex flex-col items-start">
                <label for="username" class="form-label">Username:</label>
                <input v-model="username" type="text" id="username" name="username" required class="form-control">
            </div>
            
            <div class="form-group flex flex-col items-start">
                <label for="password" class="form-label">Password:</label>
                <input v-model="password" type="password" id="password" name="password" required class="form-control">
            </div>
            
            <button @click.prevent="submitLogin">Log In</button>
        </div>
    </div>
</template>

<script>
import { gql } from "@apollo/client/core";
import { client } from "../scripts/api_access/apollo_client";


export default {
    data() {
        return{
            username: "",
            password: "",
            LOGIN_MUTATION: gql`
            mutation Login($username: String!, $password: String!) {
                login(username: $username, password: $password) {
                token
                employeeId
                message
                }
            }`,

            
        }
    },
    methods: {
        async submitLogin() {
            console.log("Button clicked, submitLogin running...");
            console.log("Username:", this.username, "Password:", this.password);

            try {
                console.log("About to call client.mutate...");
                const result = await client.mutate({
                    mutation: this.LOGIN_MUTATION,
                    variables: { username: this.username, password: this.password },
                });
                console.log("Mutation result:", result);

                const loginData = result.data.login;
                if (loginData.token) {
                    localStorage.setItem('sessionToken', loginData.token);
                    localStorage.setItem('employee_id', loginData.employeeId);
                    console.log("Login successful, data stored in localStorage!");
                } else {
                    alert(loginData.message || "Login failed.");
                }
            } catch (error) {
                console.error("Error during mutation:", error);
            }
    }

    }
}
</script>