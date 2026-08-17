const db = require("./database");

console.log("Resetting user login attempts and account lockout status...");

db.run(
  "UPDATE users SET login_attempts = 0, locked_until = NULL",
  function (err) {
    if (err) {
      console.error("Error resetting lockout status:", err.message);
      process.exit(1);
    }
    console.log(`Successfully reset account lockout status for ${this.changes} user(s).`);
    process.exit(0);
  }
);
