// Function to delete a transaction
function deleteBudgetItem(budgetID) {
  if (!confirm("Are you sure you want to delete this budget item?")) return;

  fetch(`/budget/${budgetID}/delete`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      document.querySelector(`tr[data-id='${budgetID}']`).remove();
      alert("Budget item deleted.");
    } else {
      alert("Error deleting budget item: " + result.error);
    }
  })
  .catch(error => {
    console.error("Delete error:", error);
    alert("An error occurred while deleting the budget item.");
  });
}