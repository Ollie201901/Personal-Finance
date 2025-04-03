// Function to delete a transaction
function deleteCategory(categoryID) {
  if (!confirm("Are you sure you want to delete this category?")) return;

  fetch(`/category/${categoryID}/delete`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      document.querySelector(`tr[data-id='${categoryID}']`).remove();
      alert("Category deleted.");
    } else {
      alert("Error deleting category: " + result.error);
    }
  })
  .catch(error => {
    console.error("Delete error:", error);
    alert("An error occurred while deleting the category.");
  });
}