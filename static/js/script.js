
// Attach event listener to the file input element
document.getElementById('importFileInput').addEventListener('change', handleFileSelect);
// Function to fetch and display entries
function fetchEntries() {
  fetch('/get_entries')
    .then(response => response.json())
    .then(data => {
      const entriesTable = document.getElementById('entriesTable').getElementsByTagName('tbody')[0];
      entriesTable.innerHTML = '';
      let totalBalance = 0;
      data.entries.forEach(entry => {
        const row = entriesTable.insertRow();
        row.insertCell(0).textContent = entry.date;
        row.insertCell(1).textContent = entry.description;
        row.insertCell(2).textContent = entry.amount.toFixed(2);
        row.insertCell(3).textContent = entry.entry_type;
        row.insertCell(4).textContent = entry.category;
        totalBalance += (entry.entry_type === 'Income' ? 1 : -1) * entry.amount;
      });
      document.getElementById('currentBalance').textContent = totalBalance.toFixed(2);
    });
}

// Function to handle form submission
document.getElementById('entryForm').addEventListener('submit', function(event) {
  event.preventDefault();
  const formData = new FormData(this);
  const data = {
    date: formData.get('entry-date'),
    description: formData.get('entry-description'),
    amount: parseFloat(formData.get('entry-amount')),
    entry_type: formData.get('entry-type'),
    category: formData.get('entry-category')
  };
  fetch('/add_entry', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      fetchEntries(); // Refresh the entries table
      this.reset(); // Reset the form
    } else {
      alert('Error adding entry.');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error adding entry.');
  });
});

// Fetch entries on page load
document.addEventListener('DOMContentLoaded', fetchEntries);
// Function to fetch and display transactions
function fetchTransactions() {
  fetch('/get_transactions')
    .then(response => response.json())
    .then(data => {
      const transactionsTable = document.getElementById('transactionsTable').getElementsByTagName('tbody')[0];
      transactionsTable.innerHTML = '';
      data.transactions.forEach(transaction => {
        const row = transactionsTable.insertRow();
        row.insertCell(0).textContent = transaction.description;
        row.insertCell(1).textContent = transaction.amount.toFixed(2);
        row.insertCell(2).textContent = transaction.transaction_type;
        row.insertCell(3).textContent = transaction.category;
        row.insertCell(4).textContent = transaction.schedule_type;
        row.insertCell(5).textContent = transaction.start_date;
        row.insertCell(6).textContent = transaction.end_date || 'N/A';
        row.insertCell(7).textContent = transaction.interval || 'N/A';
      });
    });
}

// Function to handle form submission
document.getElementById('transactionForm').addEventListener('submit', function(event) {
  event.preventDefault();
  const formData = new FormData(this);
  const data = {
    description: formData.get('description'),
    amount: parseFloat(formData.get('amount')),
    transaction_type: formData.get('transaction_type'),
    category: formData.get('category'),
    schedule_type: formData.get('schedule_type'),
    start_date: formData.get('start_date'),
    end_date: formData.get('end_date') || null,
    interval: formData.get('schedule_type') === 'Recurring' ? parseInt(formData.get('interval'), 10) : null
  };
  fetch('/add_transaction', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      fetchTransactions(); // Refresh the transactions table
      this.reset(); // Reset the form
    } else {
      alert('Error adding transaction.');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error adding transaction.');
  });
});

// Fetch transactions on page load
document.addEventListener('DOMContentLoaded', fetchTransactions);
