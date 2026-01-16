// API Base URL
const API_URL = 'http://localhost:8000';

// Global state
let authToken = localStorage.getItem('authToken');
let currentUser = null;
let allTransactions = [];

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    if (authToken) {
        checkAuth();
    }
    
    // Auto-calculate total in transaction form
    const quantityInput = document.getElementById('quantity');
    const priceInput = document.getElementById('price-per-share');
    const totalInput = document.getElementById('total-amount');
    
    if (quantityInput && priceInput && totalInput) {
        [quantityInput, priceInput].forEach(input => {
            input.addEventListener('input', () => {
                const quantity = parseFloat(quantityInput.value) || 0;
                const price = parseFloat(priceInput.value) || 0;
                const total = quantity * price;
                totalInput.value = `$${total.toFixed(2)}`;
            });
        });
    }
});

// Auth functions
async function register(event) {
    event.preventDefault();
    
    const email = document.getElementById('register-email').value;
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, username, password })
        });
        
        if (response.ok) {
            showNotification('¡Cuenta creada exitosamente! Ahora inicia sesión.', 'success');
            showTab('login');
            document.querySelector('#register-tab form').reset();
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Error al registrar usuario', 'error');
        }
    } catch (error) {
        showNotification('Error de conexión con el servidor', 'error');
    }
}

async function login(event) {
    event.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            localStorage.setItem('authToken', authToken);
            
            showNotification('¡Inicio de sesión exitoso!', 'success');
            checkAuth();
        } else {
            showNotification('Usuario o contraseña incorrectos', 'error');
        }
    } catch (error) {
        showNotification('Error de conexión con el servidor', 'error');
    }
}

async function checkAuth() {
    try {
        const response = await fetch(`${API_URL}/auth/me`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            currentUser = await response.json();
            showApp();
        } else {
            logout();
        }
    } catch (error) {
        logout();
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    
    document.getElementById('auth-section').style.display = 'flex';
    document.getElementById('app-section').style.display = 'none';
    document.getElementById('user-info').style.display = 'none';
    
    showNotification('Sesión cerrada', 'info');
}

function showApp() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('app-section').style.display = 'block';
    document.getElementById('user-info').style.display = 'flex';
    document.getElementById('username-display').textContent = `Hola, ${currentUser.username}`;
    
    loadTransactions();
    loadPortfolio();
}

// Tab functions
function showTab(tabName) {
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    document.querySelector(`[onclick="showTab('${tabName}')"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

function showSection(sectionName) {
    document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.section').forEach(section => section.classList.remove('active'));
    
    document.querySelector(`[onclick="showSection('${sectionName}')"]`).classList.add('active');
    document.getElementById(`${sectionName}-section`).classList.add('active');
    
    if (sectionName === 'transactions') {
        loadTransactions();
    } else if (sectionName === 'portfolio') {
        loadPortfolio();
    }
}

// Transaction functions
async function createTransaction(event) {
    event.preventDefault();
    
    const transactionData = {
        stock_symbol: document.getElementById('stock-symbol').value.toUpperCase(),
        stock_name: document.getElementById('stock-name').value || null,
        transaction_type: document.getElementById('transaction-type').value,
        quantity: parseFloat(document.getElementById('quantity').value),
        price_per_share: parseFloat(document.getElementById('price-per-share').value),
        notes: document.getElementById('notes').value || null
    };
    
    try {
        const response = await fetch(`${API_URL}/transactions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(transactionData)
        });
        
        if (response.ok) {
            showNotification('Transacción creada exitosamente', 'success');
            document.querySelector('#add-transaction-section form').reset();
            document.getElementById('total-amount').value = '';
            showSection('transactions');
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Error al crear transacción', 'error');
        }
    } catch (error) {
        showNotification('Error de conexión con el servidor', 'error');
    }
}

async function loadTransactions() {
    const listContainer = document.getElementById('transactions-list');
    listContainer.innerHTML = '<p class="loading">Cargando transacciones...</p>';
    
    try {
        const response = await fetch(`${API_URL}/transactions/`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            allTransactions = await response.json();
            displayTransactions(allTransactions);
        } else {
            listContainer.innerHTML = '<p class="loading">Error al cargar transacciones</p>';
        }
    } catch (error) {
        listContainer.innerHTML = '<p class="loading">Error de conexión</p>';
    }
}

function displayTransactions(transactions) {
    const listContainer = document.getElementById('transactions-list');
    
    if (transactions.length === 0) {
        listContainer.innerHTML = '<p class="loading">No hay transacciones registradas</p>';
        return;
    }
    
    listContainer.innerHTML = transactions.map(t => `
        <div class="transaction-card ${t.transaction_type}">
            <div class="transaction-info">
                <h3>${t.stock_symbol}</h3>
                <p>${t.stock_name || 'Sin nombre'}</p>
                <p style="font-size: 12px; color: #999;">${new Date(t.transaction_date).toLocaleString('es-ES')}</p>
            </div>
            <div class="transaction-type">
                <span class="badge ${t.transaction_type}">
                    ${t.transaction_type === 'buy' ? 'Compra' : 'Venta'}
                </span>
                <p style="margin-top: 8px; color: #666;">${t.quantity} acciones</p>
            </div>
            <div class="transaction-amount">
                <p class="amount">$${t.total_amount.toFixed(2)}</p>
                <p class="price">@ $${t.price_per_share.toFixed(2)}/acción</p>
            </div>
            <div>
                <button class="btn btn-danger" onclick="deleteTransaction(${t.id})">Eliminar</button>
            </div>
        </div>
    `).join('');
}

function filterTransactions() {
    const symbolFilter = document.getElementById('filter-symbol').value.toUpperCase();
    const typeFilter = document.getElementById('filter-type').value;
    
    const filtered = allTransactions.filter(t => {
        const matchesSymbol = !symbolFilter || t.stock_symbol.includes(symbolFilter);
        const matchesType = !typeFilter || t.transaction_type === typeFilter;
        return matchesSymbol && matchesType;
    });
    
    displayTransactions(filtered);
}

async function deleteTransaction(id) {
    if (!confirm('¿Estás seguro de eliminar esta transacción?')) return;
    
    try {
        const response = await fetch(`${API_URL}/transactions/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            showNotification('Transacción eliminada', 'success');
            loadTransactions();
            loadPortfolio();
        } else {
            showNotification('Error al eliminar transacción', 'error');
        }
    } catch (error) {
        showNotification('Error de conexión', 'error');
    }
}

// Portfolio functions
async function loadPortfolio() {
    try {
        // Load totals
        const totalsResponse = await fetch(`${API_URL}/portfolio/total`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (totalsResponse.ok) {
            const totals = await totalsResponse.json();
            displayTotals(totals);
        }
        
        // Load holdings
        const summaryResponse = await fetch(`${API_URL}/portfolio/summary`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (summaryResponse.ok) {
            const holdings = await summaryResponse.json();
            displayHoldings(holdings);
        }
    } catch (error) {
        console.error('Error loading portfolio:', error);
    }
}

function displayTotals(totals) {
    document.getElementById('total-current-value').textContent = `$${totals.total_current_value.toFixed(2)}`;
    document.getElementById('total-invested').textContent = `$${totals.total_invested.toFixed(2)}`;
    
    const profitLossElement = document.getElementById('total-profit-loss');
    const percentageElement = document.getElementById('total-percentage');
    
    profitLossElement.textContent = `$${totals.total_profit_loss.toFixed(2)}`;
    percentageElement.textContent = `${totals.total_profit_loss_percentage.toFixed(2)}%`;
    
    // Add color based on profit/loss
    if (totals.total_profit_loss >= 0) {
        profitLossElement.classList.add('positive');
        profitLossElement.classList.remove('negative');
        percentageElement.classList.add('positive');
        percentageElement.classList.remove('negative');
    } else {
        profitLossElement.classList.add('negative');
        profitLossElement.classList.remove('positive');
        percentageElement.classList.add('negative');
        percentageElement.classList.remove('positive');
    }
}

function displayHoldings(holdings) {
    const holdingsContainer = document.getElementById('portfolio-holdings');
    
    if (holdings.length === 0) {
        holdingsContainer.innerHTML = '<p class="loading">No tienes acciones en tu portfolio</p>';
        return;
    }
    
    holdingsContainer.innerHTML = holdings.map(h => `
        <div class="holding-card">
            <div class="holding-header">
                <div>
                    <h3>${h.stock_symbol}</h3>
                    <p class="shares">${h.total_shares} acciones</p>
                </div>
                <div style="text-align: right;">
                    <p style="color: #999; font-size: 12px;">${h.stock_name || 'Sin nombre'}</p>
                </div>
            </div>
            <div class="holding-stats">
                <div class="stat">
                    <p class="stat-label">Precio Promedio</p>
                    <p class="stat-number">$${h.average_buy_price.toFixed(2)}</p>
                </div>
                <div class="stat">
                    <p class="stat-label">Valor Actual</p>
                    <p class="stat-number">$${h.current_value.toFixed(2)}</p>
                </div>
                <div class="stat">
                    <p class="stat-label">Invertido</p>
                    <p class="stat-number">$${h.total_invested.toFixed(2)}</p>
                </div>
                <div class="stat">
                    <p class="stat-label">Ganancia/Pérdida</p>
                    <p class="stat-number ${h.profit_loss >= 0 ? 'positive' : 'negative'}">
                        $${h.profit_loss.toFixed(2)}
                    </p>
                </div>
                <div class="stat">
                    <p class="stat-label">Retorno</p>
                    <p class="stat-number ${h.profit_loss_percentage >= 0 ? 'positive' : 'negative'}">
                        ${h.profit_loss_percentage.toFixed(2)}%
                    </p>
                </div>
            </div>
        </div>
    `).join('');
}

// Notification function
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}
