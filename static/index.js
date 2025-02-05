function validateForm() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirm_password")?.value;

    if (username.length < 4) {
        document.getElementById("error_username").innerText = "Username must be at least 4 characters.";
        return false;
    } else {
        document.getElementById("error_username").innerText = "";
    }

    if (password.length < 6) {
        document.getElementById("error_password").innerText = "Password must be at least 6 characters.";
        return false;
    } else {
        document.getElementById("error_password").innerText = "";
    }

    if (confirmPassword && confirmPassword !== password) {
        document.getElementById("error_confirm").innerText = "Passwords do not match.";
        return false;
    } else {
        document.getElementById("error_confirm").innerText = "";
    }

    return true;
}
