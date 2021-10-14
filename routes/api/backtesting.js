const express = require("express");
const { spawn } = require("child_process");
const router = express.Router();

//@route 	GET api/backtesting/getbacktesting
//@desc 	Get a dummy Backtest
//@access 	Public

const pathToBacktest = "./test.py";

router.get("/getbacktesting", (req, res) => {
  var dataToSend = "";
  const python = spawn("python", [pathToBacktest]);
  python.stdout.on("data", (data) => {
    console.log("Fetching data from Python");
    dataToSend = data.toString();
  });
  python.on("close", (code) => {
    // console.log(`${code}`); if you want the closing code
    // respond to Browser
    res.send(dataToSend);
  });
});

module.exports = router;
