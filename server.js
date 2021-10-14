const express = require("express");

const port = process.env.PORT || 5000;
const app = express();

bt = require("./routes/api/backtesting");

app.use("/api/backtesting", bt);

app.listen(port, () => console.log(`Server started on Port ${port}`));
