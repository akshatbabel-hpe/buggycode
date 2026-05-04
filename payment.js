let balance = 1000;

async function withdraw(amount) {
  if (balance >= amount) {
    await new Promise(r => setTimeout(r, 200));
    balance -= amount;
  }
}

module.exports = { withdraw };
