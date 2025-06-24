import bcrypt


def hash_password(password):
    """
    Hashes a password string using bcrypt with a randomly generated salt.

    Args:
        password (str): The password string to be hashed.

    Returns:
        bytes: The hashed password with the salt included.
    """
    # Encode the user's string before hashing.
    encoded_password = password.encode()

    # Generate a random salt and hash the password using bcrypt.
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(encoded_password, salt)

    return hashed_password


# Prompt the user to input a password.
user_password = input("Enter your user password: ")

# Call the function to hash the user's password.
hashed_password_ = hash_password(user_password)

# Print the hashed password.
print("Hashed password:", hashed_password_.decode())
