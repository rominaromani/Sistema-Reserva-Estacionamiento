<template>
  <NavBar :user="this.$store.state.user.nombres"></NavBar>
  <router-view></router-view>
</template>

<script>
import NavBar from "./components/NavBar.vue";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

export default {
  data() {
    return {};
  },
  mounted() {
    this.token = this.$store.state.user.token;
    console.log(this.$store.state.auth);
    if (this.token !== null) {
      console.log(this.token);
      fetch(
        "http://lb-parcial-347173395.us-east-1.elb.amazonaws.com:5001/session",
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + this.token,
          },
          body: JSON.stringify({
            correo: this.$store.state.user.correo,
          }),
        }
      )
        .then((response) => response.json())
        .then((data) => {
          if (!data.success) {
            this.$store.commit("logout");
            this.$router.push("/");
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }
  },
  components: {
    NavBar,
  },
};
</script>

<style>
#app {
  font-family: Verdana, Geneva, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  --main-color: #4ecca3;
  --secundary-color: #393e46;
  --bg-color: #232931;
  --bg-secundary-color: #eeeeee;
  text-align: center;
  color: #eeeeee;
  background-color: #232931;
  min-width: 550px;
}

nav {
  padding: 30px;
}

.nav-link {
  margin: 15px;
  text-decoration: none;
  font-weight: bold;
  color: #eeeeee;
}
.router-link-exact-active {
  color: #4ecca3 !important;
}

.form-control:focus {
  box-shadow: 0 0 0 0.2rem #eeeeee;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>
