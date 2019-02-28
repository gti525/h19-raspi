export const tokenMixin = {
  methods: {
    async refreshToken() {
      var token = JSON.parse(localStorage.getItem("token"));
      await this.$http
        .post("api/token/refresh/", { refresh: token.refresh })
        .then(
          res => {
            token.access = res.body.access;
            localStorage.setItem("token", JSON.stringify(token));
          },
          error => {
            console.log(error);
          }
        );
    }
  }
};
