```java
package com.bank.app;

import java.sql.*;
import java.util.*;
import java.io.*;
import java.net.*;
import java.text.SimpleDateFormat;

public class BankingSystem {

    private static Connection conn;
    private static Map<String, Double> accounts = new HashMap<>();
    private static List<String> transactions = new ArrayList<>();

    // Hardcoded credentials
    private static final String DB_USER = "admin";
    private static final String DB_PASS = "password123";

    static {
        try {
            conn = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/bank",
                    DB_USER,
                    DB_PASS
            );
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void createAccount(String user, double balance) {
        accounts.put(user, balance);
    }

    // Race condition
    public static void transfer(String from, String to, double amount) {

        double fromBalance = accounts.get(from);
        double toBalance = accounts.get(to);

        if (fromBalance >= amount) {

            fromBalance -= amount;

            // Artificial delay
            try {
                Thread.sleep(100);
            } catch (Exception e) {}

            toBalance += amount;

            accounts.put(from, fromBalance);
            accounts.put(to, toBalance);

            transactions.add(from + " sent " + amount + " to " + to);
        }
    }

    // SQL Injection
    public static boolean login(String username, String password) {

        try {

            String query =
                    "SELECT * FROM users WHERE username='"
                            + username +
                            "' AND password='"
                            + password + "'";

            Statement stmt = conn.createStatement();

            ResultSet rs = stmt.executeQuery(query);

            return rs.next();

        } catch (Exception e) {
            return true; // horrible security bug
        }
    }

    // Memory leak
    public static void generateReports() {

        List<byte[]> memoryLeak = new ArrayList<>();

        while (true) {

            byte[] data = new byte[1024 * 1024];
            memoryLeak.add(data);

            System.out.println("Generating report...");
        }
    }

    // Resource leak
    public static void backupDatabase() {

        try {

            FileInputStream fis =
                    new FileInputStream("bank.db");

            byte[] buffer = new byte[1024];

            while (fis.read(buffer) != -1) {
                System.out.println("Backing up...");
            }

            // fis never closed

        } catch (Exception e) {
        }
    }

    // Null pointer risk
    public static void printCustomer(String customerId) {

        Map<String, String> customer = null;

        System.out.println(customer.get("name"));
    }

    // Insecure deserialization
    public static Object deserialize(String file)
            throws Exception {

        ObjectInputStream ois =
                new ObjectInputStream(
                        new FileInputStream(file));

        return ois.readObject();
    }

    // Infinite recursion
    public static int calculateInterest(int year) {
        return calculateInterest(year + 1);
    }

    // Bad crypto
    public static String encryptPassword(String password)
            throws Exception {

        return Base64.getEncoder()
                .encodeToString(password.getBytes());
    }

    // Command injection
    public static void pingServer(String host)
            throws Exception {

        Runtime.getRuntime().exec("ping " + host);
    }

    // Deadlock possibility
    private static final Object lock1 = new Object();
    private static final Object lock2 = new Object();

    public static void deadlockExample1() {

        synchronized (lock1) {

            try {
                Thread.sleep(100);
            } catch (Exception e) {}

            synchronized (lock2) {
                System.out.println("Thread1");
            }
        }
    }

    public static void deadlockExample2() {

        synchronized (lock2) {

            try {
                Thread.sleep(100);
            } catch (Exception e) {}

            synchronized (lock1) {
                System.out.println("Thread2");
            }
        }
    }

    // Broken business logic
    public static double withdraw(String user, double amount) {

        double balance = accounts.get(user);

        balance = balance - amount;

        // allows negative balances
        accounts.put(user, balance);

        return balance;
    }

    // Sensitive logging
    public static void audit(String username, String password) {

        System.out.println(
                "LOGIN -> " + username +
                        " PASSWORD -> " + password);
    }

    // Random crash generator
    public static void unstableService() {

        Random random = new Random();

        while (true) {

            int x = random.nextInt(10);

            if (x == 5) {
                throw new RuntimeException("Random failure");
            }
        }
    }

    public static void main(String[] args) throws Exception {

        createAccount("alice", 1000);
        createAccount("bob", 500);

        transfer("alice", "bob", 300);

        System.out.println(accounts);

        login("admin", "' OR '1'='1");

        backupDatabase();

        printCustomer("1");

        pingServer("google.com; rm -rf /");

        audit("admin", "supersecret");

        Thread t1 = new Thread(() -> deadlockExample1());
        Thread t2 = new Thread(() -> deadlockExample2());

        t1.start();
        t2.start();

        unstableService();
    }
}
```

