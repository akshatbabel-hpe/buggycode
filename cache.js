const cache = [];

function add(data) {
  cache.push(data);
}

function get() {
  return cache;
}

module.exports = { add, get };
