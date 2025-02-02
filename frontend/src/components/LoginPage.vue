<template>
    <div class="h-full w-full flex justify-center items-center">
        <div class="h-1/2 w-3/11">
            <div class="login-form-container h-full w-full rounded-xl shadow shadow-black flex flex-col justify-center items-center space-y-4">
                <!-- TODO: Replace logo with vector version -->
                <img src="../assets/fsea_logo.png" alt="FSEA Logo" class="form-logo">
                
                <div id="loginForm" class="space-y-3 w-5/6">
                    <div class="form-group flex flex-col items-start h-1/3 w-full space-y-2">
                        <label for="username" class="form-label">Username:</label>
                        <input @keyup.enter="submitLogin" v-model="username" type="text" id="username" name="username" required class="form-control h-1/2 w-full rounded-sm p-2 border-1">
                    </div>
                    
                    <div class="form-group flex flex-col items-start h-1/3 w-full space-y-2">
                        <label for="password" class="form-label">Password:</label>
                        <input @keyup.enter="submitLogin" v-model="password" type="password" id="password" name="password" required class="form-control h-1/2 w-full rounded-sm p-2 border-1">
                    </div>
                    
                    <!-- Container to Prevent Shifting -->
                    <div class="h-10 w-full flex justify-center">
                        <button v-if="!loading" @click.prevent="submitLogin" class="w-full h-full bg-blue-500 text-white my-2 rounded flex items-center justify-center">Log In</button>
                        <LoadSpinner v-else class="h-full my-2"/>
                        
                    </div>
                    <div class="h-10 w-full flex justify-center">
                        <div v-if="loginFailed" class="text-red-500">Access Denied</div>
                        
                    </div>
                    
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import { gql } from "@apollo/client/core";
import { client } from "../scripts/api_access/apollo_client";
import { useRouter } from "vue-router";
import LoadSpinner from "./Dashboard/animations/LoadSpinner.vue";

export default {
    components: { LoadSpinner },
    data() {
        return{
            router: useRouter(),
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
            loading: false,
            loginFailed: false,
        }
    },
    methods: {
        async submitLogin() {
            this.loginFailed = false;
            this.loading = true;
            try {
                const result = await client.mutate({
                    mutation: this.LOGIN_MUTATION,
                    variables: { username: this.username, password: this.password },
                });

                const loginData = result.data.login;
                if (loginData.token) {
                    localStorage.setItem('sessionToken', loginData.token);
                    localStorage.setItem('employee_id', loginData.employeeId);
                    this.router.push("/dashboard");
                    
                } 
            } catch (error) {
                console.error("Error during mutation:", error);
            }finally{
                this.loading = false;
                this.loginFailed = true;
            }
    }

    }
}
</script>