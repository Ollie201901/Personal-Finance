// Function to delete a transaction
function deleteTransactionSource(transactionSourceId) {
  if (!confirm("Are you sure you want to delete this transaction source?")) return;

  fetch(`/transaction_sources/${transactionSourceId}/delete`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      // Optionally, remove the row from the table
      document.querySelector(`tr[data-id='${transactionSourceId}']`).remove();
      alert("Transaction deleted.");
    } else {
      alert("Error deleting file source: " + result.error);
    }
  })
  .catch(error => {
    console.error("Delete error:", error);
    alert("An error occurred while deleting the file source.");
  });
}