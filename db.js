function getUser(email) {
  const query = "SELECT * FROM users WHERE email = '" + email + "'";
  return query;
}

module.exports = { getUser };
