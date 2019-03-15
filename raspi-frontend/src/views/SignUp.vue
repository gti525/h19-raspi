<template>
  <div id="signUpConainer">
    <div v-if="errors">
      <span
        class="alert alert-danger"
        v-for="(error, index) in errors"
        :key="`error-${index}`"
      >{{ error }}</span>
    </div>
    <div class="sign-up">
      <div class="side-panel left-panel">
        <h1>Gestion de Salle</h1>
        <h4>3 semaines d'innovations</h4>
      </div>
      <div class="side-panel right-panel">
        <div id="signUpFormContainer">
          <h2>Connexion</h2>
          <form id="signUpForm" v-on:submit="onSubmit()">
            <div class="form-data-row">
              <input type="text" v-model="username" placeholder="Nom d'utilisateur">
            </div>
            <div class="form-data-row">
              <input type="password" v-model="password" placeholder="Nouveau mot de passe">
            </div>
            <div id="signUpBtnContainer">
              <b-button type="submit" size="lg" @click="onSubmit()" id="signUpBtn">Connecter</b-button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "sign-up",
  mounted: onLoad,
  data() {
    return {
      username: "",
      password: "",
      errors: ""
    };
  },
  methods: {
    onSubmit() {
      const formData = {
        username: this.username,
        password: this.password
      };
      this.$http
        .post("api/token/", formData)
        .then(res => {
          localStorage.setItem("token", JSON.stringify(res.body));
          this.$router.push({ path: "/venues" });
        })
        .catch(error => (this.errors = error.body.non_field_errors));
    }
  },
  beforeRouteLeave(from, to, next) {
    document.getElementById("app").classList.remove("sign-up");
    next();
  }
};

function onLoad() {
  document.getElementById("app").classList.add("sign-up");
  initListeners();
}

function initListeners() {
  document.getElementById("signUpForm").onsubmit = e => {
    let isValidForm = true;
    for (let elem of e.srcElement) {
      if (elem.tagName == "INPUT" && !elem.value.trim()) {
        elem.classList.add("invalid-form-data");
        isValidForm = false;
      } else {
        elem.classList.remove("invalid-form-data");
      }
    }
    if (!isValidForm) {
      e.preventDefault();
    }
  };
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Acme");

#signUpBtn {
  margin: 0.8rem 0;
  padding-left: 2rem;
  padding-right: 2rem;
}

#signUpBtn + div {
  vertical-align: middle;
}

#signUpBtnContainer {
  text-align: left;
  padding-left: 0.5rem;
}

#signUpBtnContainer > * {
  display: inline-block;
}

#signUpBtnContainer > div {
  margin-left: 2rem;
}

div.form-data-row {
  display: block;
  width: 100%;
  padding: 0.5rem 0 0.3rem 0;
  position: relative;
}

div.form-data-row.multiple-data > input {
  width: calc(50% - 1rem) !important;
}

div.form-data-row > input {
  display: inline-block;
  margin: 0 0.5rem;
  width: calc(100% - 1rem);
  padding-left: 8px;
  border-radius: 8px;
  height: 43.5px;
  border: 1px solid darkgray;
}

div.form-data-row > input.invalid-form-data {
  border: 1px solid #ff4136 !important;
}

div.form-data-row > input:focus {
  outline: none; /* so no rectangle around rounded edges */
  border: 1px solid #0074d9;
}

#signUpFormContainer {
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 2rem;
  padding: 1rem 1.5rem;
  height: 280px;
  width: 495px;
  display: inline-block;
  position: relative;
}

#signUpFormContainer > h2,
#signUpFormContainer > h5 {
  text-align: left;
  padding-left: 0.5rem;
}

#signUpFormContainer > h2 {
  margin-top: 0.5rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);
}

#signUpFormContainer > h5 {
  margin-bottom: 1rem;
  text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.6);
}

div.side-panel {
  display: table-cell;
  vertical-align: middle;
  width: 50%;
  background-color: rgba(0, 0, 0, 0.3);
}

div.side-panel > div {
  display: block;
  width: 100%;
  padding: 0 2rem;
}

div.side-panel.left-panel h1 {
  font-size: 3rem !important;
  margin-bottom: 0;
  margin-top: -10px;
}

div.side-panel.left-panel {
  color: #fafafa;
  font-family: "Acme", sans-serif;
  text-shadow: 2px 2px 5px black;
  background-image: url("~@/assets/logo.png");
  background-position: center;
  background-repeat: no-repeat;
  background-size: 300px 260px;
}

div.sign-up {
  display: table;
  position: relative;
  height: 100%;
  width: 100%;
}

#signUpConainer {
  width: 100%;
  height: calc(100% - 85px);
}
</style>
