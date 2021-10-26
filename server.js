const dotenv = require("dotenv");

/*Configure the path for env variables */
dotenv.config({
  path: "./utils/config.env",
});

const path = require("path");
/*Module for uploading file */
const express = require("express");
// const http = require("http");
const cors = require("cors");
const colors = require("colors");

const app = express();

/*Enable cors*/
app.use(cors());

/*Middleware function to use request.body */
app.use(express.json());

//Serve static asset in production
if (process.env.NODE_ENV === "production") {
  //Set static folder
  app.use(express.static("client/build"));
  app.get("*", (req, res) => {
    res.sendFile(path.resolve(__dirname, "client", "build", "index.html"));
  });
}
app.listen(process.env.PORT || 5000, () => {
  console.log(process.env.PORT)
  console.log(`Server running at post ${process.env.PORT}`.cyan.inverse);
});