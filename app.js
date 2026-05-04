// app.js
const express = require("express");
const app = express();
app.use(express.json());

let balance = 1000;

// Fake DB
const db = {
  users: [
    { id: 1, email: "test@test.com", password: "1234", role: "user" }
  ]
};

// 🔴 LOGIN API (SQL Injection + bad auth)
app.post("/login", (req, res) => {
  const { email, password } = req.body;

  const query = `SELECT * FROM users WHERE email='${email}' AND password='${password}'`;

  console.log("Executing:", query);

  const user = db.users.find(
    u => u.email === email && u.password === password
  );

  if (user) {
    res.send({ message: "Login success", user });
  } else {
    res.status(401).send("Invalid credentials");
  }
});

// 🔴 WITHDRAW API (Race condition)
app.post("/withdraw", async (req, res) => {
  const { amount } = req.body;

  if (balance >= amount) {
    await new Promise(r => setTimeout(r, 200)); // simulate delay
    balance -= amount;
    res.send({ balance });
  } else {
    res.status(400).send("Insufficient funds");
  }
});

// 🔴 BULK SAVE (async bug)
app.post("/bulk", async (req, res) => {
  const items = req.body.items;

  items.forEach(async (item) => {
    await saveItem(item); // ❌ not awaited properly
  });

  res.send("Saved");
});

async function saveItem(item) {
  return new Promise(resolve => setTimeout(resolve, 100));
}

// 🔴 ADMIN DELETE (auth bug)
app.delete("/admin/deleteAll", (req, res) => {
  const user = req.body.user;

  if (user.role = "admin") { // ❌ bug here
    db.users = [];
    res.send("Deleted all users");
  } else {
    res.status(403).send("Forbidden");
  }
});

app.listen(3000, () => console.log("Server running"));
