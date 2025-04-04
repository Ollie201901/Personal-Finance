// Function to delete a transaction
function deleteAutoAssign(autoID) {
  if (!confirm("Are you sure you want to delete this auto-assignment?")) return;

  fetch(`/auto_categorization/${autoID}/delete`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      document.querySelector(`tr[data-id='${autoID}']`).remove();
      alert("Auto-assignment deleted.");
    } else {
      alert("Error deleting auto-assignment: " + result.error);
    }
  })
  .catch(error => {
    console.error("Delete error:", error);
    alert("An error occurred while deleting the auto-assignment.");
  });
}