// Password Strength Indicator
document.getElementById('registerPassword').addEventListener('input', function () {
    const strengthMeter = document.getElementById('passwordStrength');
    const strengthBar = strengthMeter.querySelector('.strength-bar');
    const strengthText = strengthMeter.querySelector('.strength-text');
    const password = this.value;
    let strength = 0;

    if (password.length >= 8) strength += 1;
    if (/[a-z]/.test(password)) strength += 1;
    if (/[A-Z]/.test(password)) strength += 1;
    if (/[0-9]/.test(password)) strength += 1;
    if (/[^A-Za-z0-9]/.test(password)) strength += 1;

    if (strength <= 2) {
        strengthBar.style.width = '20%';
        strengthBar.style.backgroundColor = 'red';
        strengthText.textContent = 'Weak';
    } else if (strength <= 4) {
        strengthBar.style.width = '60%';
        strengthBar.style.backgroundColor = 'orange';
        strengthText.textContent = 'Moderate';
    } else {
        strengthBar.style.width = '100%';
        strengthBar.style.backgroundColor = 'green';
        strengthText.textContent = 'Strong';
    }
});

// Toggle Password Visibility
function togglePassword(id) {
    const passwordField = document.getElementById(id);
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
    } else {
        passwordField.type = 'password';
    }
}


const spendingCtx = document.getElementById('spendingChart').getContext('2d');
const spendingChart = new Chart(spendingCtx, {
    type: 'bar',
    data: {
        labels: ['January', 'February', 'March', 'April'],
        datasets: [{
            label: 'Spending ($)',
            data: [500, 300, 400, 700],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const orderHistoryCtx = document.getElementById('orderHistoryChart').getContext('2d');
const orderHistoryChart = new Chart(orderHistoryCtx, {
    type: 'line',
    data: {
        labels: ['January', 'February', 'March', 'April'],
        datasets: [{
            label: 'Orders',
            data: [5, 10, 3, 8],
            fill: false,
            borderColor: 'rgba(153, 102, 255, 1)',
            tension: 0.1
        }]
    }
});
