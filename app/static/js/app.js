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
    // Initialize stock info auto-fill after a short delay
    setTimeout(handleStockSymbolInput, 500);
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
    loadWatchlistFromStorage();
}

// Tab functions
function showTab(tabName) {
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    document.querySelector(`[onclick="showTab('${tabName}')"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

function showSection(sectionName) {
    // Remove active class from all tabs and sections
    document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.section').forEach(section => section.classList.remove('active'));
    
    // Add active class to selected tab and section
    const selectedTab = document.querySelector(`[onclick="showSection('${sectionName}')"]`);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    const selectedSection = document.getElementById(`${sectionName}-section`);
    if (selectedSection) {
        selectedSection.classList.add('active');
    }
    
    // Load data for specific sections
    if (sectionName === 'transactions') {
        loadTransactions();
    } else if (sectionName === 'portfolio') {
        loadPortfolio();
    } else if (sectionName === 'watchlist') {
        loadWatchlistFromStorage();
        displayWatchlist();
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

// Fetch current price from API
async function fetchCurrentPrice(symbol) {
    try {
        const response = await fetch(`${API_URL}/stocks/price/${symbol}`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            const data = await response.json();
            return data.current_price;
        }
        return null;
    } catch (error) {
        console.error('Error fetching price:', error);
        return null;
    }
}

// Fetch stock info from API
async function fetchStockInfo(symbol) {
    try {
        console.log(`Fetching info for ${symbol} with token:`, authToken ? 'Present' : 'Missing');
        
        const response = await fetch(`${API_URL}/stocks/info/${symbol}`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        console.log(`Response status for ${symbol}:`, response.status);
        
        if (response.ok) {
            const data = await response.json();
            console.log(`Data for ${symbol}:`, data);
            return data;
        }
        
        const errorData = await response.json();
        console.error(`Error response for ${symbol}:`, errorData);
        return null;
    } catch (error) {
        console.error('Error fetching stock info:', error);
        return null;
    }
}

// Auto-fill stock name and price when symbol is entered
let symbolTimeout;
function handleStockSymbolInput() {
    const symbolInput = document.getElementById('stock-symbol');
    const nameInput = document.getElementById('stock-name');
    const priceInput = document.getElementById('price-per-share');
    
    if (symbolInput) {
        symbolInput.addEventListener('input', () => {
            // Clear previous timeout
            clearTimeout(symbolTimeout);
            
            // Set new timeout (wait 800ms after user stops typing)
            symbolTimeout = setTimeout(async () => {
                const symbol = symbolInput.value.toUpperCase().trim();
                
                if (symbol.length >= 1) {
                    symbolInput.value = symbol;
                    
                    if (symbol.length >= 2) {
                        showNotification('Buscando información de ' + symbol + '...', 'info');
                        
                        const info = await fetchStockInfo(symbol);
                        
                        if (info && info.current_price) {
                            // Fill company name
                            if (info.name && nameInput) {
                                nameInput.value = info.name;
                            }
                            
                            // Fill current price
                            if (priceInput) {
                                priceInput.value = info.current_price.toFixed(2);
                                
                                // Auto-calculate total
                                const quantityInput = document.getElementById('quantity');
                                if (quantityInput && quantityInput.value) {
                                    const quantity = parseFloat(quantityInput.value) || 0;
                                    const price = parseFloat(priceInput.value) || 0;
                                    const totalInput = document.getElementById('total-amount');
                                    if (totalInput) {
                                        totalInput.value = `$${(quantity * price).toFixed(2)}`;
                                    }
                                }
                            }
                            
                            showNotification(`✓ ${symbol}: $${info.current_price.toFixed(2)}`, 'success');
                        } else {
                            showNotification(`Símbolo ${symbol} no encontrado`, 'error');
                        }
                    }
                }
            }, 800); // Wait 800ms after last keystroke
        });
    }
}

// ==================== WATCHLIST FUNCTIONS ====================

// Watchlist storage (localStorage)
let watchlist = [];

// Load watchlist from localStorage
function loadWatchlistFromStorage() {
    const stored = localStorage.getItem('watchlist');
    if (stored) {
        try {
            watchlist = JSON.parse(stored);
            console.log('Watchlist loaded:', watchlist);
        } catch (e) {
            console.error('Error loading watchlist:', e);
            watchlist = [];
        }
    } else {
        watchlist = [];
    }
}

// Save watchlist to localStorage
function saveWatchlistToStorage() {
    try {
        localStorage.setItem('watchlist', JSON.stringify(watchlist));
        console.log('Watchlist saved:', watchlist);
    } catch (e) {
        console.error('Error saving watchlist:', e);
    }
}

// Add stock to watchlist
async function addToWatchlist(event) {
    event.preventDefault();
    event.stopPropagation();
    
    console.log('addToWatchlist called');
    
    const symbolInput = document.getElementById('watchlist-symbol');
    if (!symbolInput) {
        console.error('watchlist-symbol input not found');
        return;
    }
    
    const symbol = symbolInput.value.toUpperCase().trim();
    console.log('Symbol to add:', symbol);
    
    if (!symbol) {
        showNotification('Por favor ingresa un símbolo válido', 'error');
        return;
    }
    
    // Check if already in watchlist
    if (watchlist.some(item => item.symbol === symbol)) {
        showNotification(`${symbol} ya está en tu lista de seguimiento`, 'error');
        return;
    }
    
    // Validate symbol and get info
    showNotification(`Validando ${symbol}...`, 'info');
    
    try {
        const info = await fetchStockInfo(symbol);
        console.log('Stock info received:', info);
        
        if (!info || !info.current_price) {
            showNotification(`Símbolo ${symbol} no encontrado`, 'error');
            return;
        }
        
        // Add to watchlist
        watchlist.push({
            symbol: symbol,
            name: info.name || symbol,
            addedAt: new Date().toISOString()
        });
        
        console.log('Added to watchlist:', watchlist);
        
        saveWatchlistToStorage();
        showNotification(`${symbol} agregado a tu lista de seguimiento`, 'success');
        
        // Clear input
        symbolInput.value = '';
        
        // Refresh display
        await displayWatchlist();
        
    } catch (error) {
        console.error('Error adding to watchlist:', error);
        showNotification('Error al agregar la acción', 'error');
    }
}

// Remove stock from watchlist
function removeFromWatchlist(symbol) {
    if (!confirm(`¿Eliminar ${symbol} de tu lista de seguimiento?`)) {
        return;
    }
    
    console.log('Removing from watchlist:', symbol);
    
    watchlist = watchlist.filter(item => item.symbol !== symbol);
    saveWatchlistToStorage();
    showNotification(`${symbol} eliminado de tu lista`, 'success');
    displayWatchlist();
}

// Display watchlist
async function displayWatchlist() {
    const container = document.getElementById('watchlist-items');
    
    if (!container) {
        console.error('watchlist-items container not found');
        return;
    }
    
    console.log('Displaying watchlist:', watchlist);
    
    if (watchlist.length === 0) {
        container.innerHTML = '<p class="watchlist-empty">No hay acciones en tu lista de seguimiento</p>';
        return;
    }
    
    container.innerHTML = '<p class="watchlist-loading">Cargando precios...</p>';
    
    try {
        // Fetch prices for all symbols
        const promises = watchlist.map(async (item) => {
            try {
                const info = await fetchStockInfo(item.symbol);
                return {
                    ...item,
                    info: info
                };
            } catch (error) {
                console.error(`Error fetching info for ${item.symbol}:`, error);
                return {
                    ...item,
                    info: null
                };
            }
        });
        
        const results = await Promise.all(promises);
        console.log('Watchlist results:', results);
        
        // Display cards
        container.innerHTML = results.map(item => {
            const info = item.info;
            
            if (!info || !info.current_price) {
                return `
                    <div class="watchlist-card">
                        <div class="watchlist-header">
                            <div>
                                <div class="watchlist-symbol">${item.symbol}</div>
                                <div class="watchlist-name">Error al cargar datos</div>
                            </div>
                            <div>
                                <button onclick="removeFromWatchlist('${item.symbol}')" class="watchlist-remove-btn">
                                    Eliminar
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            }
            
            // Calculate change
            const previousClose = info.previous_close || info.current_price;
            const change = info.current_price - previousClose;
            const changePercent = (change / previousClose) * 100;
            const changeClass = change >= 0 ? 'positive' : 'negative';
            const changeSymbol = change >= 0 ? '+' : '';
            
            return `
                <div class="watchlist-card">
                    <div class="watchlist-header">
                        <div>
                            <div class="watchlist-symbol">${item.symbol}</div>
                            <div class="watchlist-name">${info.name || 'Sin nombre'}</div>
                        </div>
                        <div class="watchlist-price">
                            <div class="watchlist-current-price">$${info.current_price.toFixed(2)}</div>
                            <div class="watchlist-change ${changeClass}">
                                ${changeSymbol}$${change.toFixed(2)} (${changeSymbol}${changePercent.toFixed(2)}%)
                            </div>
                        </div>
                    </div>
                    
                    <div class="watchlist-info">
                        <div class="watchlist-info-item">
                            <div class="watchlist-info-label">Apertura</div>
                            <div class="watchlist-info-value">$${(info.open || 0).toFixed(2)}</div>
                        </div>
                        <div class="watchlist-info-item">
                            <div class="watchlist-info-label">Máximo</div>
                            <div class="watchlist-info-value">$${(info.day_high || 0).toFixed(2)}</div>
                        </div>
                        <div class="watchlist-info-item">
                            <div class="watchlist-info-label">Mínimo</div>
                            <div class="watchlist-info-value">$${(info.day_low || 0).toFixed(2)}</div>
                        </div>
                        <div class="watchlist-info-item">
                            <div class="watchlist-info-label">Cierre Ant.</div>
                            <div class="watchlist-info-value">$${(info.previous_close || 0).toFixed(2)}</div>
                        </div>
                    </div>
                    
                    <div class="watchlist-actions">
                        <button onclick="removeFromWatchlist('${item.symbol}')" class="watchlist-remove-btn">
                            🗑️ Eliminar
                        </button>
                    </div>
                </div>
            `;
        }).join('');
        
        // Add refresh time
        const refreshTime = new Date().toLocaleTimeString('es-ES');
        container.innerHTML += `<p class="watchlist-refresh-time">Última actualización: ${refreshTime}</p>`;
        
    } catch (error) {
        console.error('Error displaying watchlist:', error);
        container.innerHTML = '<p class="watchlist-empty">Error al cargar la lista de seguimiento</p>';
    }
}

// Refresh watchlist prices
async function refreshWatchlist() {
    showNotification('Actualizando precios...', 'info');
    await displayWatchlist();
    showNotification('Precios actualizados', 'success');
}
