// Function to delete a vendor
function deleteVendor(vendorID) {
  if (!confirm("Are you sure you want to delete this vendor?")) return;

  fetch(`/vendor/${vendorID}/delete`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      document.querySelector(`tr[data-id='${vendorID}']`).remove();
      alert("Vendor deleted.");
    } else {
      alert("Error deleting vendor: " + result.error);
    }
  })
  .catch(error => {
    console.error("Delete error:", error);
    alert("An error occurred while deleting the vendor.");
  });
}