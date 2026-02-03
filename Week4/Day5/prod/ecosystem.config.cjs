module.exports = {
  apps: [
    {
      name: "week4-api",
      script: "./server.js",
      instances: 1,
      watch: false,
      env: {
        NODE_ENV: "local",
        PORT: 3000
      },
      env_production: {
        NODE_ENV: "production",
        PORT: 3000
      }
    },
    {
      name: "week4-worker",
      script: "./src/jobs/email.worker.js",
      instances: 1,
      watch: false,
      env: {
        NODE_ENV: "local"
      },
      env_production: {
        NODE_ENV: "production"
      }
    }
  ]
};
