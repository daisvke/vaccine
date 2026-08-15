<?php
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>SQL Injection Lab</title>
    <link rel="stylesheet" href="style.css">
</head>

<body>

<h1>SQL Injection Lab</h1>

<section>
    <h2>GET — Numeric parameter</h2>

    <form action="user.php" method="get">
        <label for="user-id">User ID:</label>
        <input
            type="text"
            id="user-id"
            name="id"
            value="1"
        >

        <button type="submit">Search</button>
    </form>
</section>


<section>
    <h2>GET — String parameter</h2>

    <form action="search.php" method="get">
        <label for="username">Username:</label>
        <input
            type="text"
            id="username"
            name="username"
            value="admin"
        >

        <button type="submit">Search</button>
    </form>
</section>


<section>
    <h2>POST — String parameter</h2>

    <form action="login.php" method="post">
        <label for="login-username">Username:</label>
        <input
            type="text"
            id="login-username"
            name="username"
            value="admin"
        >

        <label for="password">Password:</label>
        <input
            type="text"
            id="password"
            name="password"
            value="test"
        >

        <button type="submit">Login</button>
    </form>
</section>


<section>
    <h2>POST — Numeric parameter</h2>

    <form action="product.php" method="post">
        <label for="product-id">Product ID:</label>
        <input
            type="text"
            id="product-id"
            name="id"
            value="1"
        >

        <button type="submit">Search</button>
    </form>
</section>

</body>
</html>
